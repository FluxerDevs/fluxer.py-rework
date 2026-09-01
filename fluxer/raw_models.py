from __future__ import annotations

from .models.reaction import (
    RawReactionActionEvent,
    RawReactionClearEmojiEvent,
    RawReactionClearEvent,
)


class RawMessageDeleteEvent:
    def __init__(self, data: dict[str, object]) -> None:
        self.message_id = int(data["id"]) if data.get("id") else None
        self.channel_id = int(data["channel_id"]) if data.get("channel_id") else None
        self.guild_id = int(data["guild_id"]) if data.get("guild_id") else None
        self.raw_data = data


class RawBulkMessageDeleteEvent:
    def __init__(self, data: dict[str, object]) -> None:
        self.message_ids = [int(value) for value in data.get("ids", data.get("message_ids", []))]
        self.channel_id = int(data["channel_id"]) if data.get("channel_id") else None
        self.guild_id = int(data["guild_id"]) if data.get("guild_id") else None
        self.raw_data = data


class RawMessageUpdateEvent:
    def __init__(self, data: dict[str, object]) -> None:
        self.message_id = int(data["id"]) if data.get("id") else None
        self.channel_id = int(data["channel_id"]) if data.get("channel_id") else None
        self.guild_id = int(data["guild_id"]) if data.get("guild_id") else None
        self.data = data
