-- DB setup for repository integration test


CREATE TABLE ports
(
    code        char(5),
    name        text NOT NULL,
    parent_slug text NOT NULL
);



CREATE TABLE prices
(
    orig_code char(5) NOT NULL,
    dest_code char(5) NOT NULL,
    day       date    NOT NULL,
    price     float   NOT NULL
);



CREATE TABLE regions
(
    slug        text NOT NULL,
    name        text NOT NULL,
    parent_slug text
);



ALTER TABLE ONLY ports
    ADD CONSTRAINT ports_pkey PRIMARY KEY (code);


--
-- Name: regions regions_pkey; Type: CONSTRAINT; Schema: tasks; Owner: -
--

ALTER TABLE ONLY regions
    ADD CONSTRAINT regions_pkey PRIMARY KEY (slug);


--
-- Name: ports ports_parent_slug_fkey; Type: FK CONSTRAINT; Schema: tasks; Owner: -
--

ALTER TABLE ONLY ports
    ADD CONSTRAINT ports_parent_slug_fkey FOREIGN KEY (parent_slug) REFERENCES regions (slug);


--
-- Name: prices prices_dest_code_fkey; Type: FK CONSTRAINT; Schema: tasks; Owner: -
--

ALTER TABLE ONLY prices
    ADD CONSTRAINT prices_dest_code_fkey FOREIGN KEY (dest_code) REFERENCES ports (code);


--
-- Name: prices prices_orig_code_fkey; Type: FK CONSTRAINT; Schema: tasks; Owner: -
--

ALTER TABLE ONLY prices
    ADD CONSTRAINT prices_orig_code_fkey FOREIGN KEY (orig_code) REFERENCES ports (code);


--
-- Name: regions regions_parent_slug_fkey; Type: FK CONSTRAINT; Schema: tasks; Owner: -
--

ALTER TABLE ONLY regions
    ADD CONSTRAINT regions_parent_slug_fkey FOREIGN KEY (parent_slug) REFERENCES regions (slug);

Insert into regions (slug, name, parent_slug)
values ('top_most_region', 'top most region', NULL),
       ('middle_region', 'middle region', 'top_most_region'),
       ('bottom_region', 'bottom region', 'middle_region'),
       ('external_region', 'external region having a single level', NULL);
INSERT into ports (code, name, parent_slug)
values ('BOTP1', 'port 1 at bottom region', 'bottom_region'),
       ('MIDP1', 'port 1 at middle region', 'middle_region'),
       ('MIDP2', 'port 2 at middle region', 'middle_region'),
       ('TOPP1', 'port 1 at top region', 'top_most_region'),
       ('EXTPP', 'port at external region', 'external_region');

INSERT INTO prices (orig_code, dest_code, day, price)
VALUES ('EXTPP', 'BOTP1', '2016-01-01', '10'),
       ('EXTPP', 'BOTP1', '2016-01-01', '12'),
       ('EXTPP', 'MIDP1', '2016-01-01', '14'),
       ('EXTPP', 'MIDP2', '2016-01-01', '16'),
       ('EXTPP', 'TOPP1', '2016-01-01', '20'),

       ('EXTPP', 'BOTP1', '2016-01-02', '10'),
       ('EXTPP', 'BOTP1', '2016-01-02', '12'),
       ('EXTPP', 'MIDP1', '2016-01-02', '14'),

       ('EXTPP', 'BOTP1', '2016-01-03', '10'),
       ('EXTPP', 'MIDP1', '2016-01-03', '12'),

       ('EXTPP', 'TOPP1', '2016-01-04', '20'),
       ('EXTPP', 'TOPP1', '2016-01-04', '25'),
       ('EXTPP', 'TOPP1', '2016-01-04', '30'),

       ('TOPP1', 'EXTPP', '2016-01-05', '100'),
       ('MIDP2', 'EXTPP', '2016-01-05', '120'),
       ('BOTP1', 'EXTPP', '2016-01-05', '130'),

       ('EXTPP', 'BOTP1', '2016-01-06', '10'),
       ('EXTPP', 'BOTP1', '2016-01-06', '12'),
       ('EXTPP', 'MIDP1', '2016-01-06', '14')