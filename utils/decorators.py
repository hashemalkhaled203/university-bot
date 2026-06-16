#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ديكوريتورز مخصصة
"""

from functools import wraps
import config
from database import db

def admin_only(func):
    """ديكوريتور للتحقق من أن المستخدم مشرف"""
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in config.ADMIN_IDS:
            await update.message.reply_text(config.MESSAGES['admin_only'])
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def member_only(func):
    """ديكوريتور للتحقق من أن المستخدم عضو"""
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if not db.is_member(user_id):
            await update.message.reply_text(
                config.MESSAGES['not_member'].format(channel=config.CHANNEL_USERNAME.lstrip('@'))
            )
            return
        return await func(update, context, *args, **kwargs)
    return wrapper
