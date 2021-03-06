-- MySQL Script generated by MySQL Workbench
-- Tue 24 Jun 2014 01:45:58 PM JST
-- Model: New Model    Version: 1.0
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema paas_manager_test
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `paas_manager_test` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `paas_manager_test` ;

-- -----------------------------------------------------
-- Table `paas_manager_test`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `paas_manager_test`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL,
  `hashed_password` CHAR(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_idx` (`email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `paas_manager_test`.`jobs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `paas_manager_test`.`jobs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `filename` VARCHAR(255) NOT NULL,
  `status` SMALLINT NOT NULL DEFAULT 0,
  `stdout` TEXT NULL,
  `stderr` TEXT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_jobs_users_idx` (`user_id` ASC),
  CONSTRAINT `fk_jobs_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `paas_manager_test`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
