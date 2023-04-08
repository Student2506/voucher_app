import React from 'react';
import { useDispatch } from "react-redux";
import { chooseVoucher } from "../../../../utils/store/changeDateSlice";

const VoucherItem = ({data}) => {

  const dispatch = useDispatch();

  return (
      <li className={"voucher-time__table_item"} onClick={() => {dispatch(chooseVoucher(data))}}>
        <p>{data.order ? data.order : "Номер заказа отсутсвует"}</p>
        <p>{data.shtrih}</p>
        <p>{`${data.issuedDate} - ${data.expiryDate}`}</p>
      </li>
  );
};

export default VoucherItem;
