import React from 'react';
import hpNotFound from "../../../images/happy_not_found.svg";
import VoucherItem from "./VoucherItem/VoucherItem";

/*
* 550 px
* */

const VoucherTime = () => {
  return (
    <div className={"voucher-time"}>
      <form className={"voucher-time__form"}>
        <h2 className={"voucher-time__title"}>Информация о выбранном сертификате:</h2>
        <p className={"voucher-time__text"}>Номер заказа <span>2212</span></p>
        <p className={"voucher-time__text"}>Штрих-код <span>32719372137213798</span></p>
        <p className={"voucher-time__text"}>Текущий срок действия <span>21.01.2002</span></p>
        <label htmlFor={"change-time"} className={"voucher-time__title"}>Обновить срок действия сертификата:</label>
        <input id={"change-time"} type={"date"} className={"input input_place_voucher-time"} defaultValue={"2023-04-07"}/>
        <button className={"button button_theme_blue"} type={"submit"}>Обновить</button>
      </form>
      <ul className={"voucher-time__table"}>
        <fieldset className={"voucher-time__filter"}>
          <input placeholder={"Поиск по номеру заказа..."} type={"text"} className={"input voucher-time__filter_item"}/>
          <input placeholder={"Поиск по штрих-коду..."} type={"text"} className={"input voucher-time__filter_item"}/>
          <input type={"date"} className={"input voucher-time__filter_item"}/>
        </fieldset>
        <div className={"voucher-time__table_title"}>
          <p>Заказ</p>
          <p>Штрих-код</p>
          <p>Текущий срок действия</p>
        </div>
        <VoucherItem />
      </ul>
    </div>
  );
};

export default VoucherTime;
