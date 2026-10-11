CREATE TABLE activity_types (
    activity_type_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    strava_type      VARCHAR(50) NOT NULL UNIQUE,
    display_name     VARCHAR(100) NOT NULL
);

CREATE TABLE activities (
    strava_id              BIGINT PRIMARY KEY,
    activity_type_id       BIGINT NOT NULL,
    name                   VARCHAR(255),
    distance_meters        DOUBLE PRECISION,
    moving_time_seconds    INTEGER,
    elapsed_time_seconds   INTEGER,
    start_date             TIMESTAMPTZ,
    start_date_local       TIMESTAMP WITHOUT TIME ZONE,
    timezone               VARCHAR(100),
    elevation_gain_meters  DOUBLE PRECISION,
    device_name            VARCHAR(255),
    manual                 BOOLEAN,
    private                BOOLEAN,
    has_heartrate          BOOLEAN,
    average_heartrate      DOUBLE PRECISION,
    max_heartrate          DOUBLE PRECISION,
    created_at             TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at             TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_activity_type
        FOREIGN KEY (activity_type_id)
        REFERENCES activity_types(activity_type_id)
);