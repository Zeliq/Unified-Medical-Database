CREATE TABLE Hospital (
  Hid int NOT NULL PRIMARY KEY,
  Hname varchar(255) NOT NULL,
  Hnum varchar(255) NOT NULL,
  Haddress varchar(255) NOT NULL
);
CREATE TABLE Doctor (
  Did int NOT NULL PRIMARY KEY,
  Dname varchar(255) NOT NULL,
  Dnum varchar(255) NOT NULL,
  DType varchar(255) NOT NULL,
  Hos_id int NOT NULL,
  FOREIGN KEY (Hos_id) REFERENCES Hospital(Hid)
);
CREATE TABLE Patient (
  Pid int NOT NULL PRIMARY KEY,
  Pname varchar(255) NOT NULL,
  Pnum varchar(255) NOT NULL,
  PAddress varchar(255) NOT NULL,
  Dr_id int NOT NULL,
  FOREIGN KEY (Dr_id) REFERENCES Doctor(Did)
);
CREATE TABLE MedicalRecord (
  Mid int NOT NULL PRIMARY KEY,
  MODE varchar(255) NOT NULL,
  Mallergies varchar(255) NOT NULL,
  Mcondition varchar(255) NOT NULL,
  Mhistory varchar(255) NOT NULL,
  Med_Id varchar(255) NOT NULL
);
CREATE TABLE Relatives (
  Rid int NOT NULL PRIMARY KEY,
  Rname varchar(255) NOT NULL,
  Rnum varchar(255) NOT NULL,
  RRelation varchar(255) NOT NULL
);
CREATE TABLE MakesRecord (
  Did int NOT NULL,
  Mid int NOT NULL,
  FOREIGN KEY (Did) REFERENCES Doctor(Did),
  FOREIGN KEY (Mid) REFERENCES MedicalRecord(Mid),
  PRIMARY KEY (Did, Mid)
);
CREATE TABLE PatientRelative (
  Pid int NOT NULL,
  Rid int NOT NULL,
  FOREIGN KEY (Pid) REFERENCES Patient(Pid),
  FOREIGN KEY (Rid) REFERENCES Relatives(Rid),
  PRIMARY KEY (Pid, Rid)
);
