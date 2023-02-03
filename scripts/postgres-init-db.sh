#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE SCHEMA IF NOT EXISTS "voucher_app";
    CREATE TABLE IF NOT EXISTS "voucher_app"."template" (
        "created" timestamp with time zone NOT NULL,
        "modified" timestamp with time zone NOT NULL,
        "id" uuid NOT NULL PRIMARY KEY,
        "title" varchar(255) NOT NULL,
        "template_content" text NOT NULL
    );
EOSQL

    