USE `paas_manager` ;
ALTER TABLE `paas_manager`.`jobs`
MODIFY COLUMN `stdout` LONGTEXT;
ALTER TABLE `paas_manager`.`jobs`
MODIFY COLUMN `stderr` LONGTEXT;

USE `paas_manager_test` ;
ALTER TABLE `paas_manager_test`.`jobs`
MODIFY COLUMN `stdout` LONGTEXT;
ALTER TABLE `paas_manager_test`.`jobs`
MODIFY COLUMN `stderr` LONGTEXT;
