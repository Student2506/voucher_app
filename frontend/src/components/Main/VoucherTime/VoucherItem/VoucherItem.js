import React from 'react';
import { useDispatch } from "react-redux";
import { chooseVoucher } from "../../../../utils/store/changeDateSlice";

const VoucherItem = ({data}) => {

  const dispatch = useDispatch();

  return (
      <li className={`voucher-time__table_item ${data.checked ? "voucher-time__table_item-checked" : ""}`} onClick={() => {dispatch(chooseVoucher(data))}}>
        <p>{data.order_id ? data.order_id : "Номер заказа отсутсвует"}</p>
        <p>{data.stock_strbarcode}</p>
        <p>{`${data.issued_date.slice(0, -8)} - ${data.expiry_date.slice(0, -8)}`}</p>
      </li>
  );
};

export default VoucherItem;
