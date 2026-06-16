#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
معالج فحص العضوية
"""

from telegram import Update, ChatMember
from telegram.ext import ContextTypes
import config
from database import db

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """فحص عضوية المستخدم في القناة"""
    user_id = update.effective_user.id
    
    try:
        # الحصول على معلومات عضوية المستخدم
        channel = config.CHANNEL_USERNAME.lstrip('@')
        member = await context.bot.get_chat_member(f"@{channel}", user_id)
        
        # التحقق من حالة العضوية
        if member.status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.CREATOR]:
            db.update_membership(user_id, True)
        else:
            db.update_membership(user_id, False)
            await update.message.reply_text(
                f"❌ عذراً! يجب عليك أن تكون عضواً في القناة أولاً.\n\n"
                f"انضم إ��ى القناة: @{channel}",
                parse_mode="Markdown"
            )
    except Exception as e:
        print(f"خطأ في فحص العضوية: {e}")
