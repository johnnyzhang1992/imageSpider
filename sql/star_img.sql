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
-- Name: star_img; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.star_img (
    id integer DEFAULT nextval('public.star_img_id_seq'::regclass) NOT NULL,
    star_id integer,
    origin character varying(32) NOT NULL,
    type character varying(128) DEFAULT NULL::character varying,
    attitudes_count integer,
    comments_count integer DEFAULT 0,
    reposts_count integer DEFAULT 0,
    is_long_text boolean DEFAULT false,
    text text,
    mid character varying(255),
    code character varying(255),
    is_video boolean DEFAULT false,
    video_url text,
    display_url text NOT NULL,
    pic_detail json,
    take_at_timestamp character varying(255),
    status character varying,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    origin_url character varying(255),
    source character varying(128),
    pid character varying(255),
    cos_url text,
    size_flag boolean DEFAULT false
);


ALTER TABLE public.star_img OWNER TO postgres;

--
-- Name: TABLE star_img; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.star_img IS '图片表';


--
-- Name: COLUMN star_img.star_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.star_id IS 'star id';


--
-- Name: COLUMN star_img.origin; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.origin IS '来源,不能为空，版权问题';


--
-- Name: COLUMN star_img.type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.type IS '图片类型，生活照剧照等';


--
-- Name: COLUMN star_img.attitudes_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.attitudes_count IS '赞，收藏';


--
-- Name: COLUMN star_img.comments_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.comments_count IS '评论数量';


--
-- Name: COLUMN star_img.reposts_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.reposts_count IS '转发数量';


--
-- Name: COLUMN star_img.is_long_text; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.is_long_text IS '是否是长文本';


--
-- Name: COLUMN star_img.text; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.text IS '内容';


--
-- Name: COLUMN star_img.mid; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.mid IS '微博id';


--
-- Name: COLUMN star_img.code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.code IS '微博pc和ins  标识码';


--
-- Name: COLUMN star_img.is_video; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.is_video IS '是否是视频';


--
-- Name: COLUMN star_img.video_url; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.video_url IS '视频地址';


--
-- Name: COLUMN star_img.display_url; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.display_url IS '图片地址';


--
-- Name: COLUMN star_img.pic_detail; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.pic_detail IS '图片详细信息，长宽大小等';


--
-- Name: COLUMN star_img.take_at_timestamp; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.take_at_timestamp IS '实际发布时间';


--
-- Name: COLUMN star_img.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.status IS '状态，private隐私、active正常、delete删除';


--
-- Name: COLUMN star_img.origin_url; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.origin_url IS '原始链接';


--
-- Name: COLUMN star_img.source; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.source IS '来源，手机型号';


--
-- Name: COLUMN star_img.cos_url; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.star_img.cos_url IS 'cos存储地址';


--
-- Name: star_img star_img_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star_img
    ADD CONSTRAINT star_img_id_key UNIQUE (id);


--
-- Name: star_img star_img_pid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star_img
    ADD CONSTRAINT star_img_pid_key UNIQUE (pid);


--
-- Name: star_img star_img_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.star_img
    ADD CONSTRAINT star_img_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

