import React, { useMemo } from 'react';
import ListItems from "../../../ListItems/ListItems";
import { getOrders } from "../../../../utils/store/ordersSlice";
import { useDispatch, useSelector } from "react-redux";

const Customers = ({ filterQuery }) => {

  const dispatch = useDispatch();
  const {selectedCustomer, customers} = useSelector(state => state.orders);

  /*Мемоизированный ответ функции фильтрации*/
  const filtredCustomers = useMemo(() => customers.filter(customer =>customer.customer_name.includes(filterQuery)), [filterQuery, customers]);

  return (
    <>
      {
        filtredCustomers.map((customer) =>
          <ListItems
            listName={"customer"}
            key={customer.customer_id}
            uniqueKey={customer.customer_id}
            title={customer.customer_name}
            value={customer.customer_id}
            checked={customer.customer_id === selectedCustomer.customer_id}
            onClickItem={(e) => {dispatch(getOrders(e.target.value))}}
          />
        )
      }
    </>
  );
};

export default Customers;
