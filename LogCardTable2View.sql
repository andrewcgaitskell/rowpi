-- View: "LocalData"."LogCardDataView"

-- DROP VIEW "LocalData"."LogCardDataView";

CREATE OR REPLACE VIEW "LocalData"."LogCardDataView" AS
 SELECT "LogCardDataText"."Name" AS rowers_name,
    to_timestamp("LogCardDataText"."RowDate"::text, 'DD/MM/YYYY'::text)::date AS row_date,
    to_timestamp("LogCardDataText"."RowTime"::text, 'HH24:MI'::text)::time without time zone AS row_time,
    "LogCardDataText"."RowName" AS row_name,
    to_timestamp("LogCardDataText"."TotalRowTime"::text, 'MI:SS.MS'::text)::time without time zone AS total_row_time,
        CASE isnumeric("LogCardDataText"."TotalRowDistance"::text)
            WHEN true THEN to_number("LogCardDataText"."TotalRowDistance"::text, '9999'::text)
            ELSE 0::numeric
        END AS total_row_distance,
        CASE isnumeric("LogCardDataText"."TotalRowAveSPM"::text)
            WHEN true THEN to_number("LogCardDataText"."TotalRowAveSPM"::text, '9999'::text)
            ELSE 0::numeric
        END AS total_row_ave_spm,
        CASE isnumeric("LogCardDataText"."TotalRowAveHR"::text)
            WHEN true THEN to_number("LogCardDataText"."TotalRowAveHR"::text, '9999'::text)
            ELSE 0::numeric
        END AS total_row_ave_hr,
    to_timestamp("LogCardDataText"."SplitTime"::text, 'MI:SS.MS'::text)::time without time zone AS split_time,
        CASE isnumeric("LogCardDataText"."SplitDistance"::text)
            WHEN true THEN to_number("LogCardDataText"."SplitDistance"::text, '9999'::text)
            ELSE 0::numeric
        END AS split_distance,
        CASE isnumeric("LogCardDataText"."SplitHR"::text)
            WHEN true THEN to_number("LogCardDataText"."SplitHR"::text, '9999'::text)
            ELSE 0::numeric
        END AS split_hr,
        CASE isnumeric("LogCardDataText"."SplitSPM"::text)
            WHEN true THEN to_number("LogCardDataText"."SplitSPM"::text, '9999'::text)
            ELSE 0::numeric
        END AS split_spm,
    to_timestamp("LogCardDataText"."Per500m"::text, 'MI:SS.MS'::text)::time without time zone AS per_500m_time,
        CASE isnumeric("LogCardDataText"."CalPerHr"::text)
            WHEN true THEN to_number("LogCardDataText"."CalPerHr"::text, '9999'::text)
            ELSE 0::numeric
        END AS cal_per_hour,
        CASE isnumeric("LogCardDataText"."WattsGenerated"::text)
            WHEN true THEN to_number("LogCardDataText"."WattsGenerated"::text, '9999'::text)
            ELSE 0::numeric
        END AS watts_generated,
        CASE isnumeric("LogCardDataText"."IntervalRestTime"::text)
            WHEN true THEN to_number("LogCardDataText"."IntervalRestTime"::text, '9999'::text)
            ELSE 0::numeric
        END AS interval_rest_time,
        CASE isnumeric("LogCardDataText"."IntervalRestDistance"::text)
            WHEN true THEN to_number("LogCardDataText"."IntervalRestDistance"::text, '9999'::text)
            ELSE 0::numeric
        END AS interval_rest_distance,
        CASE isnumeric("LogCardDataText"."IntervalRestHR"::text)
            WHEN true THEN to_number("LogCardDataText"."IntervalRestHR"::text, '9999'::text)
            ELSE 0::numeric
        END AS interval_rest_hr,
    "LogCardDataText"."UniqueRowID" AS unique_row_id
   FROM "LocalData"."LogCardDataText";

ALTER TABLE "LocalData"."LogCardDataView"
    OWNER TO andrewgaitskell;
