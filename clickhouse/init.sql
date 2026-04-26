CREATE DATABASE IF NOT EXISTS auth;

CREATE TABLE IF NOT EXISTS auth.user_events
(
    user_id Nullable(Int),
    anonymus_user_id Nullable(String),
    type String,
    timestamp DateTime,
    user_agent String,
    ip String
)
ENGINE = MergeTree
ORDER BY (timestamp);