import React, { useEffect, useMemo, useState } from 'react';
import styles from '../../../styles/changeDateVouchers.scss'
import StatusSpan from "../../StatusSpan/StatusSpan";
import { useDispatch, useSelector } from "react-redux";
import { getVouchers, selectVoucher, selectVouchers, updateExpiryDate } from "../../../utils/store/changeDateSlice";
import TableItems from "./elements/TableItems";
import LoadingScreen from "../../LoadingScreen/LoadingScreen";

const ChangeDateVouchers = () => {

  const dispatch = useDispatch();
  const {loggedIn} = useSelector(state => state.user);
  const { vouchers, status } = useSelector(state => state.changeDate);

  const [orderQuery, setOrderQuery] = useState('');
  const [barcodeQuery, setBarcodeQuery] = useState('');
  const [date, setDate] = useState('');
  const [filtredVouchers, setFiltredvouchers] = useState([]);

  useEffect(() => {
    if (loggedIn && vouchers.length === 0) {
      dispatch(getVouchers());
    }
  }, [loggedIn])

  useEffect(() => {
    searchVouchers();
  }, [vouchers])

  function searchVouchers() {
    if (orderQuery || barcodeQuery.length === 16) {
      const filtredArr = vouchers.filter((el) => {
        if (el.order_id === null && orderQuery === '') {
          return true;
        } else {
          return String(el.order_id).includes(orderQuery);
        }
      }).filter((el) => {
        return el.stock_strbarcode.includes(barcodeQuery)
      })
      setFiltredvouchers(filtredArr);
    }
  }

  function selectAll(e)  {
    const barcodesArr = filtredVouchers.map((el) => {return el.stock_strbarcode});
    dispatch(selectVouchers({ barcodes: barcodesArr, checked: e.target.checked }));
  }

  function selectOne(e) {
    dispatch(selectVoucher(e.target.value))
  }

  function updateDate() {
    const barcodesArr = filtredVouchers.filter((el) => el.checked).map((el) => {return el.stock_strbarcode});
    dispatch(updateExpiryDate({date: date, barcodes: barcodesArr}))
  }

  return (
    <section className={"change"}>

      <aside className={"change__sidebar"}>
        <div className={"change__search"}>
          <label className={"change__label"}>Номер заказа:</label>
          <input disabled={status === 'loading'} placeholder={"Введите номер заказа"} className={"change__input"} type={"text"} maxLength={10} value={orderQuery} onChange={(e) => setOrderQuery(e.target.value)}/>
          <label className={"change__label"}>Штрих-код:</label>
          <input disabled={status === 'loading'} placeholder={"Введите штрих-код"} className={"change__input"} type={"text"} maxLength={16} minLength={16} value={barcodeQuery} onChange={(e) => setBarcodeQuery(e.target.value)}/>
          <button className={"button_theme_blue change__button"} onClick={searchVouchers} disabled={orderQuery === '' && barcodeQuery === ''}>Поиск</button>
        </div>

        <div className={"change__date"}>
          <label className={"change__label"}>Укажите оконачание срока действия до даты:</label>
          <input type={"date"} className={"change__input"} value={date} onChange={(e) => setDate(e.target.value)}/>
          <StatusSpan status={status} rejectedMessage={"Упс... что-то пошло не так"} resolvedMessage={"Дата успешно обновлена"}/>
          <button className={"button_theme_blue change__button"} onClick={updateDate} disabled={date === ''}>Обновить</button>
        </div>
      </aside>

      <div className={"change__table"}>
        <div className={"change__table_header"}>
          <input type={"checkbox"} onChange={selectAll}/>
          <p className={"change__table_title"}>Заказ:</p>
          <p className={"change__table_title"}>Штрих-код:</p>
          <p className={"change__table_title"}>Действителен до даты:</p>
        </div>

        <TableItems vouchers={filtredVouchers} onChange={selectOne}/>

      </div>
      {
        status === 'loading' && <LoadingScreen />
      }
    </section>
  );
};

export default ChangeDateVouchers;
