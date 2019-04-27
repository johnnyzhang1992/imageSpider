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
-- Name: star; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.star (
    id integer DEFAULT nextval('public.star_id_seq'::regclass) NOT NULL,
    domain character varying(64) NOT NULL,
    name character varying(128) NOT NULL,
    description character varying(255),
    avatar character varying(255),
    gender character varying(1),
    follow_count integer DEFAULT 0,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    country character varying(64),
    profession character varying(128),
    baike character varying(255),
    en_name character varying(128),
    birthday date,
    status character varying(32) DEFAULT 'active'::character varying,
    wb_id character varying(255),
    ins_name character varying,
    wb_domain character varying,
    ins_id character varying(255),
    twitter_domain character varying(255),
    fb_domain character varying(255),
    tag character varying(255)
);


ALTER TABLE public.star OWNER TO postgres;

--
-- Name: TABLE star; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.star IS '明星信息表';


--
-- Name: COLUMN star.domain; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.domain IS '域名';


--
-- Name: COLUMN star.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.name IS '名字';


--
-- Name: COLUMN star.description; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.description IS '简单介绍，64字以内';


--
-- Name: COLUMN star.avatar; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.avatar IS '头像';


--
-- Name: COLUMN star.gender; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.gender IS '性别;f女,m男';


--
-- Name: COLUMN star.follow_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.follow_count IS '关注者';


--
-- Name: COLUMN star.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.created_at IS '创建时间';


--
-- Name: COLUMN star.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.updated_at IS '更新时间';


--
-- Name: COLUMN star.country; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.country IS '国家';


--
-- Name: COLUMN star.profession; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.profession IS '职业';


--
-- Name: COLUMN star.baike; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.baike IS '百度百科';


--
-- Name: COLUMN star.en_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.en_name IS '英文名字';


--
-- Name: COLUMN star.birthday; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.birthday IS '出生日期,1992-03-06';


--
-- Name: COLUMN star.wb_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.wb_id IS '微博id';


--
-- Name: COLUMN star.ins_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.ins_name IS 'ins_name';


--
-- Name: COLUMN star.wb_domain; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.wb_domain IS '微博domain';


--
-- Name: COLUMN star.ins_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.ins_id IS 'ins_id';


--
-- Name: COLUMN star.twitter_domain; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.twitter_domain IS 'twitter;https://twitter/{}';


--
-- Name: COLUMN star.fb_domain; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.fb_domain IS 'https://www.facebook.com/{}';


--
-- Name: COLUMN star.tag; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star.tag IS '标签';


--
-- Name: star star_domain_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_domain_key UNIQUE (domain);


--
-- Name: star star_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_id_key UNIQUE (id);


--
-- Name: star star_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_pkey PRIMARY KEY (id);


--
-- Name: star star_twitter_domain_fb_domain_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_twitter_domain_fb_domain_key UNIQUE (twitter_domain, fb_domain);


--
-- Name: star star_wb_id_ins_name_ins_id_wb_domain_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_wb_id_ins_name_ins_id_wb_domain_key UNIQUE (wb_id, ins_name, ins_id, wb_domain);


--
-- PostgreSQL database dump complete
--

