import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import { BASE_URL } from "../../constants";

export const getCustomers = createAsyncThunk(
  'orders/getCustomers',
  async function(_,{rejectWithValue, dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    try {
      const res = await fetch(`${BASE_URL}/api/v1/customers`, {
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `JWT ${jwt}`,
        }
      })
      if (!res.ok) throw new Error(`Ошибка при получении данных`);
      const data = await res.json();
      dispatch(addCustomers(data.results))
    } catch (err) {
      return rejectWithValue(err);
    }
  }
)

export const getOrders = createAsyncThunk(
  'orders/getOrders',
  async function(id, {rejectWithValue, dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    try{
      const res = await fetch(`${BASE_URL}/api/v1/customers/${id}/`, {
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `JWT ${jwt}`,
        }
      })
      if(!res.ok) throw new Error(`Ошибка при получении данных`);
      const data = await res.json();
      dispatch(selectCustomer(id));
      dispatch(addOrders(data));
    } catch (err) {
      return rejectWithValue(err);
    }
  }
)

export const getTemplates = createAsyncThunk(
  'orders/getTemplates',
  async function(id, {rejectWithValue, dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    dispatch(clearStatus());
    try {
      const res = await fetch(`${BASE_URL}/api/v1/order_items/${id}`, {
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `JWT ${jwt}`,
        }
      })
      if(!res.ok) throw new Error(`Ошибка при получении данных`)
      const data = await res.json();
      dispatch(addTemplates(data));
    } catch (err) {
      return rejectWithValue(err);
    }
  }
)

export const sendVoucher = createAsyncThunk(
  'orders/sendVoucher',
  async function({ orderId, emails, template }, {rejectWithValue, dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    dispatch(clearStatus());
    try {
      const res = await fetch(`${BASE_URL}/api/v1/order_item/${orderId}/`, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `JWT ${jwt}`,
        },
        body: JSON.stringify({
          "template": template,
          "addresses": emails,
        })
      })
      if (!res.ok) throw new Error(`Что-то пошло не так`)
    } catch (err) {
      return rejectWithValue(err.message)
    }
  }
)

const ordersSlice = createSlice({
  name: 'orders',
  initialState: {
    customers: [],
    selectedCustomer: {},
    orders: [],
    templates: [],
    status: null,
    error: null,
    pushStatus: null,
    pushError: null,
  },
  reducers: {
    // Добавление списка покупателей
    addCustomers: (state, action) => {
      state.customers = action.payload;
    },
    // Выбор покупателя по ID
    selectCustomer: (state, action) => {
      state.selectedCustomer = state.customers.find(customer => customer.customer_id === Number(action.payload));
    },
    // Добавление заказов
    addOrders: (state, action) => {
      state.orders = action.payload.orders;
      state.templates = [];
    },
    // Добавление шаблонов
    addTemplates: (state, action) => {
      // Преобразование данных в массив
      state.templates = Object.entries(action.payload.templates).map((e) => ( { [e[0]]: e[1] } ));
    },
    // Очистка статусов и ошибок
    clearStatus: (state) => {
      state.status = null;
      state.error = null;
      state.pushError = null;
      state.pushStatus = null;
    },
  },
  extraReducers: {
    // Обработка отправки купона
    [sendVoucher.pending]: (state) => {
      state.pushStatus = 'loading';
      state.pushError = null;
    },
    [sendVoucher.fulfilled]: (state) => {
      state.pushStatus = 'resolved';
    },
    [sendVoucher.rejected]: (state, action) => {
      state.pushStatus = 'rejected';
      state.pushError = action.payload;
    },
    [getCustomers.pending]: (state) => {
      state.status = 'loading';
    },
    [getCustomers.fulfilled]: (state) => {
      state.status = null;
    },
    [getCustomers.rejected]: (state) => {
      state.status = 'rejected';
    },
    [getOrders.pending]: (state) => {
      state.status = 'loading-orders';
    },
    [getOrders.fulfilled]: (state) => {
      state.status = null;
    },
    [getOrders.rejected]: (state) => {
      state.status = 'rejected';
    },
  },
});

export const {addCustomers, addOrders, addTemplates, clearStatus, selectCustomer} = ordersSlice.actions;

export default ordersSlice.reducer;
