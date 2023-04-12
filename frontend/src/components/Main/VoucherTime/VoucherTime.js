import React, { useEffect, useMemo, useState } from 'react';
import hpNotFound from "../../../images/happy_not_found.svg";
import VoucherItem from "./VoucherItem/VoucherItem";
import { useDispatch, useSelector } from "react-redux";
import { getVouchers, pushNewExpiryDate } from "../../../utils/store/changeDateSlice";
import LoadingScreen from "../../LoadingScreen/LoadingScreen";

/*
* 550 px
* */

const VoucherTime = () => {

  const dispatch = useDispatch();
  const { vouchers, checkedVoucher } = useSelector(state => state.changeDate);
  const status = useSelector(state => state.status.status);

  const [changeDate, setChangeDate] = useState('');
  const [orderId, setOrderId] = useState('');
  const [shtrih, setShtrih] = useState('');

  useEffect(() => {
    dispatch(getVouchers())
  }, [])

  function submit(e) {
    e.preventDefault();
    dispatch(pushNewExpiryDate(changeDate));
  }

  console.log(vouchers.find((voucher) => voucher.stock_strbarcode === "2222900000015644"));

  const vouchersArr = useMemo(() => {
    if (orderId !== '' || shtrih !== '') {
      const fArr = vouchers.filter((voucher) => String(voucher.order_id).includes(orderId));
      return fArr.filter((voucher) => voucher.stock_strbarcode.includes(shtrih));
    } else {
      return vouchers;
    }
  }, [shtrih, orderId, vouchers])

  return (
    <div className={"voucher-time"}>
      <form className={"voucher-time__form"} onSubmit={submit}>
        <h2 className={"voucher-time__title"}>Информация о выбранном сертификате:</h2>
        <p className={"voucher-time__text"}>Номер заказа <span>{`${checkedVoucher.order_id ? checkedVoucher.order_id : ""}`}</span></p>
        <p className={"voucher-time__text"}>Штрих-код <span>{`${checkedVoucher.stock_strbarcode ? checkedVoucher.stock_strbarcode : ""}`}</span></p>
        <p className={"voucher-time__text"}>Текущий срок действия <span>{`${checkedVoucher.expiry_date ? checkedVoucher.expiry_date.slice(0, -8) : ""}`}</span></p>
        <label htmlFor={"change-time"} className={"voucher-time__title"}>Обновить срок действия сертификата:</label>
        <input id={"change-time"} type={"date"} className={"input input_place_voucher-time"} value={changeDate} onChange={(e) => {setChangeDate(e.target.value)}}/>
        <button className={"button button_theme_blue"} type={"submit"}>Обновить</button>
      </form>
      <ul className={"voucher-time__table"}>
        <fieldset className={"voucher-time__filter"}>
          <input placeholder={"Поиск по номеру заказа..."} value={orderId} onChange={(e) => setOrderId(e.target.value)} type={"text"} className={"input voucher-time__filter_item"} />
          <input placeholder={"Поиск по штрих-коду..."} value={shtrih} onChange={(e) => setShtrih(e.target.value)} type={"text"} className={"input voucher-time__filter_item"} />
          <input type={"date"} className={"input voucher-time__filter_item"} />
        </fieldset>
        <div className={"voucher-time__table_title"}>
          <p>Заказ</p>
          <p>Штрих-код</p>
          <p>Текущий срок действия</p>
        </div>
        {
          vouchersArr.map((voucher, i) =>
            <VoucherItem
              data={voucher}
              key={i}
            />
          )
        }
      </ul>
      {
        status === 'loading' ? <LoadingScreen /> : <></>
      }
    </div>
  );
};

export default VoucherTime;
