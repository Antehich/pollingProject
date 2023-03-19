import asyncio
import logging
import sys
import os
from dotenv import load_dotenv


from aiogram import Bot, types, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


form_router = Router()
load_dotenv('.env')
token = os.getenv('token')
bot = Bot(token)


class Form(StatesGroup):
    educationalStep = State()
    yearOfEducation = State()
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()
    q9 = State()
    q10 = State()
    q11 = State()
    q12 = State()
    q13 = State()


async def append_data(data):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '17cezUu5ZOAdZuGjWMLgmPEfyc97Phx2LMmaYSqQEj9g'
    range_ = 'A1:D1'
    value_input_option = 'USER_ENTERED'
    insert_data_option = 'INSERT_ROWS'
    value_range_body = {
                                                            "majorDimension": "ROWS",
                                                            "values": [
                                                                [
                                                                    f"{data['educationalStep']}",
                                                                    f"{data['yearOfEducation']}",
                                                                    f"{data['q1']}",
                                                                    f"{data['q2']}"
                                                                ]
                                                            ]
                                                        }

    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)


@form_router.message(Command("start"))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.educationalStep)
    await message.answer(
        "Привет! На какой ступени обучения ты находишься?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Бакалавриат"),
                    KeyboardButton(text="Магистратура"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.educationalStep, F.text == "Бакалавриат")
async def process_bachelor(message: Message, state: FSMContext) -> None:
    await state.update_data(educationalStep=message.text)
    print(123)
    await state.set_state(Form.yearOfEducation)

    await message.answer(
        "Супер! А на каком году обучения?\nКстати, ты можешь отменить текущие ответы просто написав cancel или /cancel в любое время.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="1"),
                    KeyboardButton(text="2"),
                    KeyboardButton(text="3"),
                    KeyboardButton(text="4"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Form.educationalStep, F.text == "Магистратура")
async def process_master(message: Message, state: FSMContext) -> None:
    await state.update_data(educationalStep=message.text)
    await state.set_state(Form.yearOfEducation)

    await message.answer(
        "Супер! А на каком году обучения?\nКстати, ты можешь отменить текущие ответы просто написав cancel или /cancel в любое время.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="1"),
                    KeyboardButton(text="2"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Form.yearOfEducation)
async def process_year_of_education(message: Message, state: FSMContext) -> None:
    await state.update_data(yearOfEducation=message.text)
    await state.set_state(Form.q1)

    await message.answer(
        "вопрос1\n"
        "1)опция1\n"
        "2)опция2\n"
        "3)опция3\n"
        "4)опция4\n",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="1"),
                    KeyboardButton(text="2"),
                    KeyboardButton(text="3"),
                    KeyboardButton(text="4"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Form.q1)
async def process_q1(message: Message, state: FSMContext) -> None:
    await state.update_data(q1=message.text)
    await state.set_state(Form.q2)

    await message.answer(
        "вопрос2\n"
        "1)опция1\n"
        "2)опция2\n"
        "3)опция3\n"
        "4)опция4\n",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="1"),
                    KeyboardButton(text="2"),
                    KeyboardButton(text="3"),
                    KeyboardButton(text="4"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Form.q2)
async def process_q2(message: Message, state: FSMContext) -> None:
    await state.update_data(q2=message.text)
    data = await state.get_data()
    await state.clear()

    await message.answer("Спасибо за твои ответы! Держи кота.", reply_markup=ReplyKeyboardRemove())
    await message.answer_photo(types.URLInputFile('https://cataas.com/cat'))
    await append_data(data)


async def main():
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
