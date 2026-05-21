--
-- Data for Name: app_businesselement; Type: TABLE DATA; Schema: public; Owner: postgres
--


COPY public.app_businesselement (id, type, code) FROM stdin;
1	order	9e82320f-85f8-490c-aaed-9fa4d9b2684c
2	product	7b6633ad-c9f1-403b-82f7-b80017918114
3	orderItem	896f2517-4082-4114-9895-d515e664aba8
\.

--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--


COPY public.auth_group (id, name) FROM stdin;
1	admin
2	user
3	manager
4	guest
\.

--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--


COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
4	pbkdf2_sha256$1200000$CHBpxOyYQUAYcSWRcagsRt$XZXWAAP3fDLIf+W4N2MAEMjOb/btP4wXAnRU4t15H68=	\N	f	H4-TuwKLraFCH1m	string	string	guest@example.com	f	t	2026-05-21 14:39:58.551731+00
2	pbkdf2_sha256$1200000$wJkTSOVfinIDk3nf2Tq8rM$xq3DlDMu4lwbIg8qXKq/Ht5tHeyRs4x/Oz/sBXxYDuk=	\N	f	g	string	string	user@example.com	f	t	2026-05-21 14:39:35+00
3	pbkdf2_sha256$1200000$ZCPIYJKYMwYLtBq9u89Etk$PCNmdAhkLcc0KgvNL65U9M6JlyGTO93iM/woYmGtafk=	\N	f	ozaD.5O+pfdC10dys3p	string	string	manager@example.com	f	t	2026-05-21 14:40:22+00
\.

--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--


COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
1	4	4
2	2	2
3	3	3
4	1	1
\.

--
-- Data for Name: app_accessgrouprule; Type: TABLE DATA; Schema: public; Owner: postgres
--


COPY public.app_accessgrouprule (id, read_permission, read_all_permission, create_permission, update_permission, update_all_permission, delete_permission, delete_all_permission, group_id, element_id) FROM stdin;
1	t	t	t	t	t	t	t	1	1
2	t	t	t	t	f	t	f	2	1
4	t	t	t	t	t	t	t	1	2
5	t	t	t	t	t	t	t	3	1
6	t	t	t	t	t	t	t	3	2
3	t	t	f	f	f	f	f	2	2
7	f	f	f	f	f	f	f	4	1
8	f	f	f	f	f	f	f	4	2
9	t	t	t	t	t	t	t	1	3
10	t	f	t	t	f	t	f	2	3
11	t	t	t	t	t	t	t	3	3
12	f	f	f	f	f	f	f	4	3
\.

--
-- Data for Name: app_product; Type: TABLE DATA; Schema: public; Owner: postgres
--


COPY public.app_product (id, name, description, element_id, creator_id, price) FROM stdin;
1	HDD	string	2	1	111111.00
2	SSD	string	2	1	22222.00
\.

--
-- Data for Name: app_order; Type: TABLE DATA; Schema: public; Owner: postgres
--


COPY public.app_order (id, element_id, creator_id, created_at) FROM stdin;
1	1	1	2026-05-21 16:26:41.897759+00
\.

--
-- Data for Name: app_orderitem; Type: TABLE DATA; Schema: public; Owner: postgres
--


COPY public.app_orderitem (id, quantity, order_id, product_id, element_id) FROM stdin;
1	2	1	1	3
\.
