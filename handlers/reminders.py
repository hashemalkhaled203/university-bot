#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
معالج التذكيرات
"""

from telegram import Update
from telegram.ext import ContextTypes
from database import db

async def manage_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """إدارة التذكيرات"""
    user_id = update.effective_user.id
    reminders = db.get_user_reminders(user_id)
    
    if not reminders:
        await update.message.reply_text(
            "❌ لم تقم بإضافة أي تذكيرات بعد.",
            parse_mode="Markdown"
        )
        return
    
    reminders_text = "⏰ **التذكيرات الخاصة بك**\n\n"
    
    for reminder in reminders:
        reminders_text += (
            f"📚 {reminder['subject']}\n"
            f"   ⏰ {reminder['start_time']} - تذكير في {reminder['reminder_time']}\n\n"
        )
    
    await update.message.reply_text(
        reminders_text,
        parse_mode="Markdown"
    )
