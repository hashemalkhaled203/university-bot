#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
معالج أوامر البداية والمساعدة
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config
from database import db

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر /start"""
    user = update.effective_user
    
    # إضافة المستخدم إلى قاعدة البيانات
    db.add_user(user.id, user.username)
    
    # إنشاء لوحة المفاتيح
    keyboard = [
        [
            InlineKeyboardButton("📅 الجدول الدراسي", callback_data="schedule"),
            InlineKeyboardButton("⏰ التذكيرات", callback_data="reminders")
        ],
        [
            InlineKeyboardButton("📝 المسابقات", callback_data="quiz"),
            InlineKeyboardButton("📊 حساب المعدل", callback_data="gpa")
        ],
        [
            InlineKeyboardButton("❓ المساعدة", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 **مرحباً {user.first_name}!**\n\n"
        "أنا بوت الجامعة الذكي 🤖\n\n"
        "اختر من القائمة أدناه:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر /help"""
    await update.message.reply_text(
        config.MESSAGES['help'],
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج نقرات الأزرار"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "schedule":
        await query.edit_message_text(
            text="📅 **الجدول الدراسي**\n\n"
                "اختر يوم الأسبوع:",
            parse_mode="Markdown"
        )
    elif query.data == "reminders":
        await query.edit_message_text(
            text="⏰ **التذكيرات**\n\n"
                "اختر عملية التذكير:",
            parse_mode="Markdown"
        )
    elif query.data == "quiz":
        await query.edit_message_text(
            text="📝 **المسابقات**\n\n"
                "اختر مادة:",
            parse_mode="Markdown"
        )
    elif query.data == "gpa":
        await query.edit_message_text(
            text="📊 **حساب المعدل**\n\n"
                "لحساب معدلك، يجب أن تكون درجاتك مسجلة في النظام.",
            parse_mode="Markdown"
        )
    elif query.data == "help":
        await query.edit_message_text(
            text=config.MESSAGES['help'],
            parse_mode="Markdown"
        )
