from fastapi import FastAPI, Request
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .database import engine, Base
from sqlalchemy import text
from . import models, crud, schemas
from .redis_client import redis_client
from .state_manager import set_state, get_state, clear_state
from twilio.twiml.messaging_response import MessagingResponse
from fastapi.responses import PlainTextResponse



models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Whatsapp Product Review Collector")

@app.get("/")
def read_root():
    return {"Message": "Success"}

    
# test endpoint to verify db connection
# @app.post("/posts")
# def create_post(payload: dict, db: Session = Depends(get_db)):
    
#     result = db.execute(text("SELECT 1")).scalar()
#     return {"ok": True, "db_check": result, "payload": payload}

@app.get("/api/reviews", response_model=list[schemas.ReviewResponse])
def get_all_reviews(db: Session = Depends(get_db)):
    reviews = crud.get_reviews(db)
    return reviews


# test endpoint to verify redis connection
@app.get("/test-redis")
def test_redis():
    try:
        redis_client.set("test_key", "hello")
        value = redis_client.get("test_key")
        return {"status": "connected", "value": value}
    except Exception as e:
        return {"status": "error", "details": str(e)}
    

# endpoint to simulate incoming WhatsApp messages without Twilio
# @app.post("/simulate")
# async def simulate_message(request: Request, db: Session = Depends(get_db)):
#     data = await request.json()
#     incoming = data.get("Body", "").strip()
#     sender = data.get("From", "").strip()

#     state = get_state(sender)

#     if state is None or incoming.lower() in ["hi", "hello", "start"]:
#         set_state(sender, "await_product")
#         return {"reply": "Which product would you like to review?"}

#     step = state["step"]

#     if step == "await_product":
#         # store product → go to next step
#         set_state(sender, "await_name", product=incoming)
#         return {"reply": "Please enter your name."}

#     if step == "await_name":
#         # store name → go to next step
#         set_state(sender, "await_review", product=state["product"], name=incoming)
#         return {"reply": f"Share your review for {state['product']}."}

#     if step == "await_review":
#         # save to database
#         review = crud.create_review(
#             db=db,
#             contact_number=sender,
#             user_name=state["name"],
#             product_name=state["product"],
#             product_review=incoming
#         )

#         clear_state(sender)
#         return {"reply": "Thank you! Your review has been recorded."}

#     return {"reply": "Something went wrong. Send Hi to start again."}


# twilio webhook endpoint
@app.post("/webhook")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    incoming = form.get("Body", "").strip()
    sender = form.get("From", "").replace("whatsapp:", "").strip()

    resp = MessagingResponse()

    state = get_state(sender)

    # start or restart flow
    if state is None or incoming.lower() in ["hi", "hello", "start"]:
        set_state(sender, "await_product")
        resp.message("Which product would you like to review?")
        return PlainTextResponse(str(resp), media_type="application/xml")

    step = state["step"]

    if step == "await_product":
        set_state(sender, "await_name", product=incoming)
        resp.message("Please enter your name.")
        return PlainTextResponse(str(resp), media_type="application/xml")

    if step == "await_name":
        set_state(sender, "await_review", product=state["product"], name=incoming)
        resp.message(f"Share your review for {state['product']}.")
        return PlainTextResponse(str(resp), media_type="application/xml")

    if step == "await_review":
        crud.create_review(
            db=db,
            contact_number=sender,
            user_name=state["name"],
            product_name=state["product"],
            product_review=incoming
        )
        clear_state(sender)
        resp.message("Thank you! Your review has been recorded.")
        return PlainTextResponse(str(resp), media_type="application/xml")

    resp.message("Something went wrong. Send Hi to start again.")
    return PlainTextResponse(str(resp), media_type="application/xml")

