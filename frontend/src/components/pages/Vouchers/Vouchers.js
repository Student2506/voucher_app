import React, { useEffect, useState } from 'react';
import SearchInput from "../../SearchInput/SearchInput";
import "../../../styles/vouchers.scss";
import { useDispatch, useSelector } from "react-redux";
import { getCustomers, getTemplates, sendVoucher } from "../../../utils/store/ordersSlice";
import Customers from "./elements/Customers";
import Orders from "./elements/Orders";
import Templates from "./elements/Templates";
import SubmitForm from "./elements/SubmitForm";
import LoadingScreen from "../../LoadingScreen/LoadingScreen";
import PagePreloader from "../../PagePreloader/PagePreloader";

const Vouchers = () => {

  const dispatch = useDispatch();

  const [checkedOrder, setCheckedOrder] = useState(null); // Сохраняет id выбранного заказа
  const [checkedTemplate, setCheckedTemplate] = useState(null); // Сохраняет id выбранного шаблона
  const [filterQueryContr, setFilterQueryContr] = useState(''); // Поле input фильтра К/А
  const [filterQueryOrders, setFilterQueryOrders] = useState('');
  const [filterQueryTemplates, setFilterQueryTemplates] = useState('');
  const [inputValues, setInputValues] = useState({}); // Поля для всех input email
  const [settingOpen, setSettingOpen] = useState(false);
  const [shareOpt, setShareOpt] = useState(false);
  const [useQR, setUseQR] = useState(false);

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
    dispatch(sendVoucher({orderId: checkedOrder, template: checkedTemplate, emails, sharepoint: shareOpt, qrcode: useQR}))
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
          value={filterQueryContr}
          onChangeInput={(e) => {setFilterQueryContr(e.target.value)}}
          onClickButton={() => {setFilterQueryContr('')}}
        />
        <div className={"vouchers__list"}>
          <Customers filterQuery={filterQueryContr} />
        </div>
      </aside>
      {
        status === 'loading-orders' ? <PagePreloader /> : Object.keys(selectedCustomer).length > 0 &&
          <>
            <div className={"vouchers__orders vouchers__container"}>
              <h2 className={"vouchers__subtitle"}>Заказы: <span className={"vouchers__subtitle_partner"}>{selectedCustomer.customer_name}</span></h2>
              <SearchInput
                type={"text"}
                placeholder={"Введите имя заказа..."}
                extraClassesContainer={"vouchers__filter"}
                value={filterQueryOrders}
                onChangeInput={(e) => {setFilterQueryOrders(e.target.value)}}
                onClickButton={() => {setFilterQueryOrders('')}}
              />
              <div className={"vouchers__container_list"}>
                <Orders
                  filterQuery={filterQueryOrders}
                  onClickItem={(e) => {
                    setCheckedOrder(e.target.value)
                    dispatch(getTemplates(e.target.value))
                  }}
                />
              </div>
            </div>
            {
              status === 'loading-templates' ? <PagePreloader /> : templates.length > 0 &&
                <div className={"vouchers__templates vouchers__container"}>
                  <h2 className={"vouchers__subtitle"}>Шаблоны:</h2>
                  <button className={"button vouchers__settings-btn"} onClick={() => {setSettingOpen(!settingOpen)}}/>

                  <div className={`vouchers__settings ${settingOpen && "vouchers__settings_open"}`}>
                    <div className={"vouchers__settings_option"}>
                      <input className={"vouchers__settings_checkbox"} type={"checkbox"} id={"share-copy"} checked={shareOpt} onChange={() => {setShareOpt(!shareOpt)}}/>
                      <label className={"vouchers__settings_label"} htmlFor={"share-copy"} />
                      <p className={"vouchers__settings_option-title"}>Создать ссылку</p>
                    </div>

                    <div className={"vouchers__settings_option"}>
                      <input className={"vouchers__settings_checkbox"} type={"checkbox"} id={"qr-check"} checked={useQR} onChange={() => {setUseQR(!useQR)}}/>
                      <label className={"vouchers__settings_label"} htmlFor={"qr-check"} />
                      <p className={"vouchers__settings_option-title"}>Использовать QR-Code</p>
                    </div>
                  </div>

                  <SearchInput
                    type={"text"}
                    placeholder={"Введите наименование шаблона..."}
                    extraClassesContainer={"vouchers__filter"}
                    value={filterQueryTemplates}
                    onChangeInput={(e) => {setFilterQueryTemplates(e.target.value)}}
                    onClickButton={() => {setFilterQueryTemplates('')}}
                  />

                  <div className={"vouchers__container_list"}>
                    <Templates onClickItem={(e) => {setCheckedTemplate(e.target.value)}} filterQuery={filterQueryTemplates}/>
                  </div>

                  <SubmitForm
                    share={shareOpt}
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
