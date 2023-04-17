import React, { useEffect, useMemo, useState } from 'react';
import notFound from "../../../images/not_found.svg";
import VoucherItem from "./VoucherItem/VoucherItem";
import { useDispatch, useSelector } from "react-redux";
import { getVouchers, pushNewExpiryDate } from "../../../utils/store/changeDateSlice";
import LoadingScreen from "../../LoadingScreen/LoadingScreen";
import circle from "../../../images/Rolling-1s-200px.svg";

/*
* 550 px
* */

const VoucherTime = () => {

  const dispatch = useDispatch();
  const { vouchers, checkedVoucher, changeDateStatus } = useSelector(state => state.changeDate);
  const status = useSelector(state => state.status.status);

  const [orderId, setOrderId] = useState('');
  const [shtrih, setShtrih] = useState('');
  const [date, setDate] = useState('');
  const [vouchersArr, setVouchersArr] = useState([]);

  useEffect(() => {
    if(vouchers.length === 0) {
      dispatch(getVouchers());
    }
  }, [])

  useEffect(() => {
    searchVouchers();
  }, [vouchers])

  function searchVouchers() {
    if (orderId || shtrih) {
      const filtredArr = vouchers.filter((el) => {
        if (el.order_id === null || orderId === '') {
          return true;
        } else {
          return String(el.order_id).includes(orderId);
        }
      }).filter((el) => {
        return el.stock_strbarcode.includes(shtrih)
      })
      setVouchersArr(filtredArr);
    }
  }

  function submit(e) {
    e.preventDefault();
    dispatch(pushNewExpiryDate(date))
  }

  return (
    <div className={"voucher-time"}>
      <form className={"voucher-time__form"} onSubmit={submit}>
        <label className={"voucher-time__label"} htmlFor={"order_input"}>Номер заказа:</label>
        <input
          value={orderId}
          onChange={e => setOrderId(e.target.value)}
          className={"input voucher-time__input"}
          type={"text"}
          id={"order_input"}
          placeholder={"Введите номер заказа"}
          max={10}
        />
        <label className={"voucher-time__label"} htmlFor={"shtrih_input"}>Штрих-код:</label>
        <input
          value={shtrih}
          onChange={e => setShtrih(e.target.value)}
          className={"input voucher-time__input"}
          type={"text"}
          id={"shtrih_input"}
          placeholder={"Введите штрих-код"}
          max={16}
        />
        <button type={"button"} className={"button button_theme_blue voucher-time__button"} onClick={searchVouchers} disabled={orderId === '' && shtrih === ''}>Поиск</button>
        <label className={"voucher-time__label"} htmlFor={"shtrih_input"}>Укажите оконачание срока действия до даты:</label>
        <input
          value={date}
          onChange={e => setDate(e.target.value)}
          className={"input voucher-time__input"}
          type={"date"}
        />
        {
          changeDateStatus === 'resolved' || changeDateStatus === 'rejected'
            ? <span
              className={`templates__progress ${changeDateStatus === 'resolved' ? "templates__progress_success" : "templates__progress_failure"}`}
            >
              {changeDateStatus === 'resolved' ? "Данные успешно обновлены" : "Что-то пошло не так, попробуйте еще раз."}
          </span>
            : <span className={"templates__progress"}></span>
        }
        <button type={"submit"} className={"button button_theme_blue voucher-time__button"} disabled={date === '' && checkedVoucher}>
          {changeDateStatus === 'loading' ? <img src={circle} className="button_preload" alt={"Обновляем..."}/> : "Обновить"}
        </button>
      </form>
      <ul className={"voucher-time__table"}>
        <div className={"voucher-time__table_title"}>
          <p>Заказ</p>
          <p>Штрих-код</p>
          <p>Текущий срок действия</p>
        </div>
        { vouchersArr.length > 0 ?
          vouchersArr.map((el, i) => {
           return <VoucherItem data={el} key={i}/>
          }) : <div className={"voucher-time__nf"}><img src={notFound}/><p>Ничего не нашлось</p></div>
        }
      </ul>
      {
        status === 'loading' ? <LoadingScreen /> : <></>
      }
    </div>
  );
};

export default VoucherTime;
