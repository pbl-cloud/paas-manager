USE `paas_manager` ;

ALTER TABLE `paas_manager`.`jobs`
ADD COLUMN (
  `arguments` VARCHAR(255),
  `retries` SMALLINT NOT NULL DEFAULT 0
);

USE `paas_manager_test` ;
ALTER TABLE `paas_manager_test`.`jobs`
ADD COLUMN (
  `arguments` VARCHAR(255),
  `retries` SMALLINT NOT NULL DEFAULT 0
);
