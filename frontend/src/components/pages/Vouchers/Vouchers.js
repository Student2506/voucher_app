import React, { useEffect, useState } from 'react';
import SearchInput from "../../SearchInput/SearchInput";
import styles from "../../../styles/vouchers.scss";
import { useDispatch, useSelector } from "react-redux";
import { getCustomers, getTemplates, sendVoucher } from "../../../utils/store/ordersSlice";
import Customers from "./elements/Customers";
import Orders from "./elements/Orders";
import Templates from "./elements/Templates";
import SubmitForm from "./elements/SubmitForm";
import LoadingScreen from "../../LoadingScreen/LoadingScreen";

const Vouchers = () => {

  const dispatch = useDispatch();

  const [checkedOrder, setCheckedOrder] = useState(null); // Сохраняет id выбранного заказа
  const [checkedTemplate, setCheckedTemplate] = useState(null); // Сохраняет id выбранного шаблона
  const [filterQuery, setFilterQuery] = useState(''); // Поле input фильтра К/А
  const [inputValues, setInputValues] = useState({}); // Поля для всех input email

  const {selectedCustomer, pushError, templates, status, customers} = useSelector(state => state.orders); // Забираем из Redux данные
  const {loggedIn} = useSelector(state => state.user); // Забираем статус пользователя из Redux

  useEffect(() => {
    if (loggedIn && customers.length === 0) {
      dispatch(getCustomers())
    }
  }, [loggedIn])

  /*Функция отправки сертификата*/
  function handleSendVoucher(e) {
    e.preventDefault();
    const emails = Object.values(inputValues).join('; '); // Переводим значения всех key объекта в строку
    dispatch(sendVoucher({orderId: checkedOrder, template: checkedTemplate, emails}))
  }

  /*Функция очистки инпута email*/
  function clearInputValue(index) {
    const { [`email-${index}`]: _, ...newInputValues } = inputValues;
    setInputValues(newInputValues);
  }

  return (
    <section className={"vouchers"}>
      <aside className={"vouchers__customers"}>
        <SearchInput
          type={"text"}
          placeholder={"Фильтр по наименованию..."}
          extraClassesContainer={"vouchers__filter"}
          value={filterQuery}
          onChangeInput={(e) => {setFilterQuery(e.target.value)}}
          onClickButton={() => {setFilterQuery('')}}
        />
        <div className={"vouchers__list"}>
          <Customers filterQuery={filterQuery} />
        </div>
      </aside>
      {
        Object.keys(selectedCustomer).length > 0 &&
          <>
            <div className={"vouchers__orders vouchers__container"}>
              <h2 className={"vouchers__subtitle"}>Заказы: <span className={"vouchers__subtitle_partner"}>{selectedCustomer.customer_name}</span></h2>
              <div className={"vouchers__container_list"}>
                <Orders
                  onClickItem={(e) => {
                    setCheckedOrder(e.target.value)
                    dispatch(getTemplates(e.target.value))
                  }}
                />
              </div>
            </div>
            {
              templates.length > 0 &&
                <div className={"vouchers__templates vouchers__container"}>
                  <h2 className={"vouchers__subtitle"}>Шаблоны:</h2>
                  <div className={"vouchers__container_list"}>
                    <Templates onClickItem={(e) => {setCheckedTemplate(e.target.value)}} />
                  </div>
                  <SubmitForm
                    disabled={!checkedTemplate}
                    onSubmit={handleSendVoucher}
                    changeInputValue={(e) => {
                      setInputValues({
                        ...inputValues,
                        [e.target.name]: e.target.value,
                      })
                    }}
                    clearInputValue={clearInputValue}
                  />
                </div>
            }
          </>
      }
      {
        Object.keys(selectedCustomer).length === 0 && <div className={"vouchers__nf"} />
      }
      {
        status === 'loading' && <LoadingScreen />
      }
    </section>
  );
};

export default Vouchers;
