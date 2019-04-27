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
-- Name: star_ins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.star_ins (
    id integer DEFAULT nextval('public.star_ins_id_seq'::regclass) NOT NULL,
    ins_id character varying(128),
    name character varying(128),
    verified boolean DEFAULT true,
    description character varying(255),
    followers_count character varying(128),
    follow_count character varying(128),
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    gender character varying(1),
    star_id integer NOT NULL,
    avatar text,
    full_name character varying(255),
    status character varying(128) DEFAULT 'active'::character varying
);


ALTER TABLE public.star_ins OWNER TO postgres;

--
-- Name: TABLE star_ins; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.star_ins IS '明星ins信息表';


--
-- Name: COLUMN star_ins.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_ins.name IS '名字';


--
-- Name: COLUMN star_ins.verified; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_ins.verified IS '是否认证';


--
-- Name: COLUMN star_ins.description; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_ins.description IS '简单介绍';


--
-- Name: COLUMN star_ins.followers_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_ins.followers_count IS '粉丝数量';


--
-- Name: COLUMN star_ins.follow_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_ins.follow_count IS '关注者';


--
-- Name: COLUMN star_ins.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_ins.created_at IS '创建时间';


--
-- Name: COLUMN star_ins.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_ins.updated_at IS '更新时间';


--
-- Name: COLUMN star_ins.gender; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_ins.gender IS '性别';


--
-- Name: star_ins star_ins_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star_ins
    ADD CONSTRAINT star_ins_id_key UNIQUE (id);


--
-- Name: star_ins star_ins_ins_id_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star_ins
    ADD CONSTRAINT star_ins_ins_id_name_key UNIQUE (ins_id, name);


--
-- Name: star_ins star_ins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star_ins
    ADD CONSTRAINT star_ins_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

