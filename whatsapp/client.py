import logging
from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv
from neonize import extract_text
from Agent.agent import create_chat, send_message, dump_history
from whatsapp.utils import init_db, load_history, save_history
from Agent.tools import create_tools
logger = logging.getLogger(__name__)

client = NewClient("whatsapp/session.db")
init_db()


@client.event(ConnectedEv)
def on_connected(client: NewClient, _: ConnectedEv) -> None:
    print("Connected")


@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv) -> None:
    source = message.Info.MessageSource

    if source.IsFromMe or source.IsGroup:
        return

    text = extract_text(message.Message)
    if not text or not text.strip():
        return

    user_id = source.Sender.User
    chat = create_chat(tools = create_tools(user_id), history = load_history(user_id))

    try:
        response = send_message(chat, text.strip())
    except Exception:
        logger.exception("Gemini call failed for %s", user_id)
        client.reply_message("Sorry, something went wrong. Please try again.", message)
        return

    save_history(user_id, dump_history(chat))
    client.reply_message(response.text or "I couldn't generate a reply.", message)