CREATE TABLE  "OFFICES" 
   (	"ID" NUMBER NOT NULL ENABLE, 
	"OFFICE_NAME" VARCHAR2(150) NOT NULL ENABLE, 
	 CONSTRAINT "OFFICES_PK" PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   )
/
CREATE TABLE  "HOSTS" 
   (	"ID" NUMBER NOT NULL ENABLE, 
	"HOSTNAME" VARCHAR2(30) NOT NULL ENABLE, 
	"IPADDRESS" VARCHAR2(20) NOT NULL ENABLE, 
	"HOST_TYPE" VARCHAR2(20) NOT NULL ENABLE, 
	"OFFICE_ID" NUMBER NOT NULL ENABLE, 
	"SNMP_ACCESS_STRING" VARCHAR2(50), 
	"SSH_USER" VARCHAR2(50), 
	"SSH_PASS" VARCHAR2(50), 
	"SUUS_ID" VARCHAR2(15), 
	 CONSTRAINT "HOSTS_PK" PRIMARY KEY ("ID")
  USING INDEX  ENABLE, 
	 CONSTRAINT "HOSTS_SUUS_ID_UNIQUE" UNIQUE ("SUUS_ID")
  USING INDEX  ENABLE, 
	 CONSTRAINT "HOSTS_TYPES_CON" CHECK ( "HOST_TYPE" IN ('IMMv1', 'IMMv2', 'XCC', 'AMM', 'FC', 'Storwize', 'PDU', 'TAPE', 'PDU_APC')) ENABLE
   )
/
CREATE TABLE  "USERS" 
   (	"ID" NUMBER, 
	"LOGIN" VARCHAR2(50) NOT NULL ENABLE, 
	"USERNAME" VARCHAR2(150) NOT NULL ENABLE, 
	"OFFICE_ID" NUMBER NOT NULL ENABLE, 
	"PASSWORD" VARCHAR2(50) NOT NULL ENABLE, 
	 CONSTRAINT "USERS_PK" PRIMARY KEY ("ID")
  USING INDEX  ENABLE, 
	 CONSTRAINT "USERS_LOGIN_UK1" UNIQUE ("LOGIN")
  USING INDEX  ENABLE
   )
/
CREATE TABLE  "XCC" 
   (	"ID" NUMBER NOT NULL ENABLE, 
	"HOST_ID" NUMBER NOT NULL ENABLE, 
	"CAPTURE_DATE" DATE, 
	"BMCACTIVE" VARCHAR2(50), 
	"UEFI" VARCHAR2(50), 
	"LXPM" VARCHAR2(50), 
	"BMCPRIMARY" VARCHAR2(50), 
	"BMCBACKUP" VARCHAR2(50), 
	"LXPMWINDOWS" VARCHAR2(50), 
	"LXPMLINUX" VARCHAR2(50), 
	 CONSTRAINT "XCC_PK" PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   )
/
CREATE TABLE  "STORWIZE" 
   (	"ID" NUMBER NOT NULL ENABLE, 
	"HOST_ID" NUMBER NOT NULL ENABLE, 
	"CAPTURE_DATE" DATE, 
	"FIRMWARE" VARCHAR2(150), 
	 CONSTRAINT "STORWIZE_PK" PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   )
/
CREATE TABLE  "FIBRECHANNEL" 
   (	"ID" NUMBER NOT NULL ENABLE, 
	"HOST_ID" NUMBER NOT NULL ENABLE, 
	"CAPTURE_DATE" DATE, 
	"FIRMWARE" VARCHAR2(50) NOT NULL ENABLE, 
	 CONSTRAINT "FIBRECHANNEL_PK" PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   )
/
CREATE TABLE  "IMM2" 
   (	"ID" NUMBER NOT NULL ENABLE, 
	"HOST_ID" NUMBER NOT NULL ENABLE, 
	"CAPTURE_DATE" DATE NOT NULL ENABLE, 
	"IMM_PRIMARY" VARCHAR2(50), 
	"IMM_BACKUP" VARCHAR2(50), 
	"IMM_ACTIVE" VARCHAR2(50), 
	"UEFI_PRIMARY" VARCHAR2(50), 
	"UEFI_BACKUP" VARCHAR2(50), 
	"UEFI_ACTIVE" VARCHAR2(50), 
	"DSA" VARCHAR2(50), 
	 CONSTRAINT "IMM2_PK" PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   )
/
CREATE TABLE  "PDU" 
   (	"ID" NUMBER, 
	"HOST_ID" NUMBER NOT NULL ENABLE, 
	"CAPTURE_DATE" DATE, 
	"FIRMWARE" VARCHAR2(50), 
	 CONSTRAINT "PDU_PK" PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   )
/
CREATE TABLE  "AMM" 
   (	"ID" NUMBER NOT NULL ENABLE, 
	"HOST_ID" NUMBER NOT NULL ENABLE, 
	"CAPTURE_DATE" DATE, 
	"BUILD1" VARCHAR2(15), 
	"BUILD2" VARCHAR2(15), 
	"REVISION1" VARCHAR2(15), 
	"REVISION2" VARCHAR2(15), 
	 CONSTRAINT "AMM_PK" PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   )
/
CREATE TABLE  "PDU_APC" 
   (	"ID" NUMBER NOT NULL ENABLE, 
	"HOST_ID" NUMBER NOT NULL ENABLE, 
	"CAPTURE_DATE" DATE, 
	"RACKPDU" VARCHAR2(20), 
	"APCOS" VARCHAR2(20), 
	"BOOTMONITOR" VARCHAR2(20), 
	 CONSTRAINT "PDU_ACC_PK" PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   )
/
CREATE TABLE  "TAPE" 
   (	"ID" NUMBER, 
	"HOST_ID" NUMBER NOT NULL ENABLE, 
	"CAPTURE_DATE" DATE, 
	"FIRMWARE" VARCHAR2(50)
   )
/
CREATE TABLE  "LOGS" 
   (	"ID" NUMBER NOT NULL ENABLE, 
	"TIMESTAMP" TIMESTAMP (6) NOT NULL ENABLE, 
	"MESSAGE" VARCHAR2(1000), 
	 CONSTRAINT "LOGS_PK" PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   )
/
ALTER TABLE  "HOSTS" ADD CONSTRAINT "HOSTS_FK" FOREIGN KEY ("OFFICE_ID")
	  REFERENCES  "OFFICES" ("ID") ENABLE
/
ALTER TABLE  "FIBRECHANNEL" ADD CONSTRAINT "FIBRECHANNEL_FK_HOSTS" FOREIGN KEY ("HOST_ID")
	  REFERENCES  "HOSTS" ("ID") ON DELETE CASCADE ENABLE
/
ALTER TABLE  "IMM2" ADD CONSTRAINT "IMM2_HOST_FK" FOREIGN KEY ("HOST_ID")
	  REFERENCES  "HOSTS" ("ID") ON DELETE CASCADE ENABLE
/
ALTER TABLE  "AMM" ADD CONSTRAINT "AMM_HOST_FK" FOREIGN KEY ("HOST_ID")
	  REFERENCES  "HOSTS" ("ID") ON DELETE CASCADE ENABLE
/
ALTER TABLE  "PDU" ADD CONSTRAINT "PDU_HOSTS_FK" FOREIGN KEY ("HOST_ID")
	  REFERENCES  "HOSTS" ("ID") ON DELETE CASCADE ENABLE
/
ALTER TABLE  "XCC" ADD CONSTRAINT "XCC_HOSTS_FK" FOREIGN KEY ("HOST_ID")
	  REFERENCES  "HOSTS" ("ID") ON DELETE CASCADE ENABLE
/
ALTER TABLE  "STORWIZE" ADD CONSTRAINT "STORWIZE_HOSTS_FK" FOREIGN KEY ("HOST_ID")
	  REFERENCES  "HOSTS" ("ID") ON DELETE CASCADE ENABLE
/
ALTER TABLE  "USERS" ADD CONSTRAINT "USERS_OFFICE_FK" FOREIGN KEY ("OFFICE_ID")
	  REFERENCES  "OFFICES" ("ID") ENABLE
/
ALTER TABLE  "TAPE" ADD CONSTRAINT "TAPE_HOSTS_FK" FOREIGN KEY ("HOST_ID")
	  REFERENCES  "HOSTS" ("ID") ON DELETE CASCADE ENABLE
/
ALTER TABLE  "PDU_APC" ADD CONSTRAINT "PDU_APC_HOSTS_FK" FOREIGN KEY ("HOST_ID")
	  REFERENCES  "HOSTS" ("ID") ON DELETE CASCADE ENABLE
/
CREATE INDEX  "FIBRECHANNEL_HOSTS_IDX1" ON  "FIBRECHANNEL" ("HOST_ID")
/
CREATE INDEX  "IMM2_HOST_IDX1" ON  "IMM2" ("HOST_ID")
/
CREATE INDEX  "PDU_HOST_IDX1" ON  "PDU" ("HOST_ID")
/
CREATE INDEX  "STORWIZE_IDX1" ON  "STORWIZE" ("HOST_ID")
/
CREATE INDEX  "TAPE_HOST_IDX1" ON  "TAPE" ("HOST_ID")
/
CREATE INDEX  "XCC_HOST_IDX1" ON  "XCC" ("HOST_ID")
/
 CREATE SEQUENCE   "HOSTS-DEV_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 41 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "OFFICES_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 21 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "HOSTS_PK_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 701 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "EMP_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 8000 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "DEPT_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 50 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "IMM2_OK_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 13961 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "FIBRECHANNEL_PK_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 10181 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "PDU_PK_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 5641 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "XCC_PK_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 8041 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "LOGS_PK_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 12561 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "AMM_PK_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 3421 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "STORWIZE_PK_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 7541 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "USERS_PK_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 141 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "TAPE_PK_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 6541 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "PDU_ACC_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 2581 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
 CREATE SEQUENCE   "HOST_TYPES_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 21 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
/
CREATE OR REPLACE EDITIONABLE TRIGGER  "BI_AMM" 
  before insert on "AMM"               
  for each row  
begin   
  if :NEW."ID" is null then 
    select "AMM_PK_SEQ".nextval into :NEW."ID" from sys.dual; 
  end if; 
end; 

/
ALTER TRIGGER  "BI_AMM" ENABLE
/
CREATE OR REPLACE EDITIONABLE TRIGGER  "BI_FIBRECHANNEL" 
  before insert on "FIBRECHANNEL"               
  for each row  
begin   
  if :NEW."ID" is null then 
    select "FIBRECHANNEL_PK_SEQ".nextval into :NEW."ID" from sys.dual; 
  end if; 
end; 

/
ALTER TRIGGER  "BI_FIBRECHANNEL" ENABLE
/
CREATE OR REPLACE EDITIONABLE TRIGGER  "BI_HOSTS" 
  before insert on "HOSTS"               
  for each row  
begin   
  if :NEW."ID" is null then 
    select "HOSTS_PK_SEQ".nextval into :NEW."ID" from sys.dual; 
  end if; 
end; 

/
ALTER TRIGGER  "BI_HOSTS" ENABLE
/
CREATE OR REPLACE EDITIONABLE TRIGGER  "BI_IMM2" 
  before insert on "IMM2"               
  for each row  
begin   
  if :NEW."ID" is null then 
    select "IMM2_OK_SEQ".nextval into :NEW."ID" from sys.dual; 
  end if; 
end; 

/
ALTER TRIGGER  "BI_IMM2" ENABLE
/
CREATE OR REPLACE EDITIONABLE TRIGGER  "BI_LOGS" 
  before insert on "LOGS"               
  for each row  
begin   
  if :NEW."ID" is null then 
    select "LOGS_PK_SEQ".nextval into :NEW."ID" from sys.dual; 
  end if; 
end; 

/
ALTER TRIGGER  "BI_LOGS" ENABLE
/
CREATE OR REPLACE EDITIONABLE TRIGGER  "BI_OFFICES" 
  before insert on "OFFICES"               
  for each row  
begin   
  if :NEW."ID" is null then 
    select "OFFICES_SEQ".nextval into :NEW."ID" from sys.dual; 
  end if; 
end; 

/
ALTER TRIGGER  "BI_OFFICES" ENABLE
/
CREATE OR REPLACE EDITIONABLE TRIGGER  "BI_PDU" 
  before insert on "PDU"               
  for each row  
begin   
  if :NEW."ID" is null then 
    select "PDU_PK_SEQ".nextval into :NEW."ID" from sys.dual; 
  end if; 
end; 

/
ALTER TRIGGER  "BI_PDU" ENABLE
/
CREATE OR REPLACE EDITIONABLE TRIGGER  "BI_PDU_ACC" 
  before insert on "PDU_APC"               
  for each row  
begin   
  if :NEW."ID" is null then 
    select "PDU_ACC_SEQ".nextval into :NEW."ID" from sys.dual; 
  end if; 
end; 

/
ALTER TRIGGER  "BI_PDU_ACC" ENABLE
/
CREATE OR REPLACE EDITIONABLE TRIGGER  "BI_STORWIZE" 
  before insert on "STORWIZE"               
  for each row  
begin   
  if :NEW."ID" is null then 
    select "STORWIZE_PK_SEQ".nextval into :NEW."ID" from sys.dual; 
  end if; 
end; 

/
ALTER TRIGGER  "BI_STORWIZE" ENABLE
/
CREATE OR REPLACE EDITIONABLE TRIGGER  "BI_TAPE" 
  before insert on "TAPE"               
  for each row  
begin   
  if :NEW."ID" is null then 
    select "TAPE_PK_SEQ".nextval into :NEW."ID" from sys.dual; 
  end if; 
end;

/
ALTER TRIGGER  "BI_TAPE" ENABLE
/
CREATE OR REPLACE EDITIONABLE TRIGGER  "BI_USERS" 
  before insert on "USERS"               
  for each row  
begin   
  if :NEW."ID" is null then 
    select "USERS_PK_SEQ".nextval into :NEW."ID" from sys.dual; 
  end if; 
end; 

/
ALTER TRIGGER  "BI_USERS" ENABLE
/
CREATE OR REPLACE EDITIONABLE TRIGGER  "BI_XCC" 
  before insert on "XCC"               
  for each row  
begin   
  if :NEW."ID" is null then 
    select "XCC_PK_SEQ".nextval into :NEW."ID" from sys.dual; 
  end if; 
end; 

/
ALTER TRIGGER  "BI_XCC" ENABLE
/
CREATE OR REPLACE EDITIONABLE TRIGGER  "USERS_PASSWORD_HASH_TR" 
BEFORE insert or update on USERS
for each row
declare
pass_hash varchar2(50);
begin
select ORA_HASH(:NEW.PASSWORD) INTO pass_hash from dual;
:NEW.PASSWORD := pass_hash;
end;

/
ALTER TRIGGER  "USERS_PASSWORD_HASH_TR" ENABLE
/