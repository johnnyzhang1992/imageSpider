--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.12
-- Dumped by pg_dump version 10.5 (Ubuntu 10.5-0ubuntu0.18.04)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: star_wb; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.star_wb (
    id integer DEFAULT nextval('public.star_wb_id_seq'::regclass) NOT NULL,
    screen_name character varying(128) NOT NULL,
    verified boolean DEFAULT true,
    verified_reason character varying(255),
    description character varying(255),
    gender character varying(1) NOT NULL,
    followers_count integer,
    follow_count integer,
    avatar text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    wb_id character varying(255) NOT NULL,
    star_id integer NOT NULL
);


ALTER TABLE public.star_wb OWNER TO postgres;

--
-- Name: TABLE star_wb; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.star_wb IS '明星微博信息表';


--
-- Name: COLUMN star_wb.screen_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_wb.screen_name IS '名字';


--
-- Name: COLUMN star_wb.verified; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_wb.verified IS '是否认证';


--
-- Name: COLUMN star_wb.verified_reason; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_wb.verified_reason IS '认证原因';


--
-- Name: COLUMN star_wb.description; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_wb.description IS '简单介绍';


--
-- Name: COLUMN star_wb.gender; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_wb.gender IS '性别;f女,m男';


--
-- Name: COLUMN star_wb.followers_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_wb.followers_count IS '粉丝数量';


--
-- Name: COLUMN star_wb.follow_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_wb.follow_count IS '关注人数';


--
-- Name: COLUMN star_wb.avatar; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_wb.avatar IS '头像';


--
-- Name: COLUMN star_wb.wb_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_wb.wb_id IS '微博id';


--
-- Name: star_wb star_wb_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star_wb
    ADD CONSTRAINT star_wb_id_key UNIQUE (id);


--
-- Name: star_wb star_wb_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star_wb
    ADD CONSTRAINT star_wb_pkey PRIMARY KEY (id);


--
-- Name: star_wb star_wb_screen_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star_wb
    ADD CONSTRAINT star_wb_screen_name_key UNIQUE (screen_name);


--
-- PostgreSQL database dump complete
--

