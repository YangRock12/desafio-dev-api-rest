-- MySQL Workbench Forward Engineering

-- -----------------------------------------------------
-- Schema dock_api
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dock_api` DEFAULT CHARACTER SET utf8mb4;
USE `dock_api` ;


-- -----------------------------------------------------
-- Table `dock_api`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dock_api`.`users` (
  `user_id` INT NOT NULL auto_increment,
  `document` varchar(16) NOT NULL UNIQUE,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dock_api`.`digital_accounts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dock_api`.`digital_accounts` (
  `digital_account_id` INT NOT NULL auto_increment,
  `digital_account_agency` INT NOT NULL,
  `user_id` INT NOT NULL,
  `total` FLOAT NOT NULL,
  `withdraw_daily_limit` FLOAT NOT NULL DEFAULT 2000,
  `is_blocked` BOOLEAN NOT NULL DEFAULT TRUE,
  `is_active` BOOLEAN NOT NULL DEFAULT FALSE,
  INDEX `fk_user_id_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_id_idx`
    FOREIGN KEY (`user_id`)
    REFERENCES `dock_api`.`users` (`user_id`),
  PRIMARY KEY (`digital_account_id`, `digital_account_agency`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

ALTER TABLE `dock_api`.`digital_accounts`
auto_increment=10000000;


-- -----------------------------------------------------
-- Table `dock_api`.`transaction_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dock_api`.`transaction_type` (
  `transaction_type_id` INT NOT NULL auto_increment,
  `transaction_type_description` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`transaction_type_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dock_api`.`financial_transactions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dock_api`.`financial_transactions` (
  `transaction_id` INT NOT NULL auto_increment,
  `digital_account_id` INT NOT NULL,
  `digital_account_agency` INT NOT NULL,
  `transaction_type_id` INT NOT NULL,
  `movement_value` FLOAT NOT NULL,
  `operation_date` DATETIME,
  INDEX `fk_digital_account_id_idx` (`digital_account_id` ASC),
  INDEX `fk_transaction_type_id_idx` (`transaction_type_id` ASC),
  CONSTRAINT `fk_digital_account_id_idx`
    FOREIGN KEY (`digital_account_id`)
    REFERENCES `dock_api`.`digital_accounts` (`digital_account_id`),
  CONSTRAINT `fk_transaction_type_id_idx`
    FOREIGN KEY (`transaction_type_id`)
    REFERENCES `dock_api`.`transaction_type` (`transaction_type_id`),
  PRIMARY KEY (`transaction_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- CREATE EVENT ON Table `dock_api`.`digital_accounts`
-- -----------------------------------------------------
CREATE EVENT IF NOT EXISTS `reset_withdraw_daily_limit`
ON SCHEDULE
  EVERY 1 DAY
  COMMENT 'Reset withdraw daily limit to 2000'
  DO
    UPDATE `dock_api`.`digital_accounts`
    SET withdraw_daily_limit = 2000;


-- -----------------------------------------------------
-- INSERT INTO Table `dock_api`.`transaction_type`
-- -----------------------------------------------------
INSERT INTO dock_api.transaction_type (transaction_type_id, transaction_type_description)
VALUES (1, "withdraw");
INSERT INTO dock_api.transaction_type (transaction_type_id, transaction_type_description)
VALUES (2, "deposit");