import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import { baseUrl } from "../../constants";
import { fulfilledFetch, pendingFetch, rejectFetch } from "./statusAppSlice";

let lastOrder;

/*Получение всех контрагентов*/
export const getCustomers = createAsyncThunk(
  'customers/getCustomers',
  async function(_, {rejectWithValue, dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    dispatch(pendingFetch());
    try {
      const res = await fetch(`${baseUrl}/api/v1/customers/`, {
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `JWT ${jwt}`,
        }
      })
      if (!res.ok) throw new Error(`Ошибка при получении данных`);
      const data = await res.json();
      const dataWithChecked = data.results.map((item) => {
        return {
          ...item,
          checked: false,
        }
      })
      dispatch(addCustomers({dataWithChecked}));
      dispatch(fulfilledFetch());
    } catch (err) {
      dispatch(rejectFetch());
    }
  }
)

/* Получение заказов выбранного контраагента */
export const getCustomerOrders = createAsyncThunk(
  'customers/getCustomerOrders',
  async function({ id }, {rejectWithValue, dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    dispatch(pendingFetch());
    try {
      const res = await fetch(`${baseUrl}/api/v1/customers/${id}/`, {
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `JWT ${jwt}`,
        }
      })
      if (!res.ok) throw new Error(`Ошибка при получении данных`);
      const data = await res.json();
      dispatch(addOrders({data}))
      dispatch(fulfilledFetch());
    } catch (err) {
      dispatch(rejectFetch());
    }
  }
)

/* Получение шаблонов для выбранного заказа */
export const getOrderTemplates = createAsyncThunk(
  'customers/getOrderTemplates',
  async function({id}, {rejectWithValue, dispatch, getState}) {
    lastOrder = id;
    const jwt = getState().user.userData.jwt.auth;
    dispatch(pendingFetch());
    try {
      const res = await fetch(`${baseUrl}/api/v1/voucher_type/${id}`, {
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `JWT ${jwt}`,
        }
      })
      if (!res.ok) throw new Error(`Ошибка при получении данных`);
      const data = await res.json();
      dispatch(addTemplates({data}));
      dispatch(fulfilledFetch());
    } catch (err) {
      dispatch(rejectFetch());
    }
  }
)

/* Отправка воучера с выбранным заказом и шаблоном */
export const pushVoucher = createAsyncThunk(
  'customers/pushVoucher',
  async function({ email, template}, {rejectWithValue, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    try {
      const res = await fetch(`${baseUrl}/api/v1/order_item/${lastOrder}/`, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `JWT ${jwt}`,
        },
        body: JSON.stringify({
          "template": template,
          "addresses": email,
        })
      })
      if (!res.ok) throw new Error(`Ошибка ${res.status}`);

    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
)

export const customersSlice = createSlice({
  name: 'customers',
  initialState: {
    customers: [],
    filteredCustomers: null,
    orders: [],
    templates: [],
    pushStatus: null,
    pushError: null,
  },
  reducers: {
    addCustomers(state, action) {
      state.customers = action.payload.dataWithChecked;
    },
    addOrders(state, action) {
      state.orders = action.payload.data.orders;
    },
    addTemplates(state, action) {
      state.templates = Object.entries(action.payload.data.templates).map((e) => ( { [e[0]]: e[1] } ));
    },
    toggleCheckedCustomer(state, action) {
      state.templates = [];
      state.orders = [];
      state.pushStatus = null;
      state.pushError = null;
      state.customers = state.customers.map((customer) => {
        return {
          ...customer,
          checked: customer.customer_id === action.payload.id,
        }
      });
    },
    setFilteredCustomers(state, action) {
      state.filteredCustomers = action.payload;
    }
  },
  extraReducers: {
    [pushVoucher.pending]: (state) => {
      state.pushStatus = 'loading';
      state.pushError = null;
    },
    [pushVoucher.fulfilled]: (state) => {
      state.pushStatus = 'resolved';
    },
    [pushVoucher.rejected]: (state, action) => {
      state.pushStatus = 'rejected';
      state.pushError = action.payload;
    }
  }
})

export const {addCustomers, addOrders, addTemplates, toggleCheckedCustomer, setFilteredCustomers} = customersSlice.actions;

export default customersSlice.reducer;
