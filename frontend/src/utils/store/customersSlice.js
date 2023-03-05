import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import { baseUrl } from "../../constants";
import { fulfilledFetch, pendingFetch, rejectFetch } from "./statusAppSlice";

let lastOrder;
let lastCustomer;

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
      dispatch(addCustomers({data}))
      dispatch(fulfilledFetch());
    } catch (err) {
      dispatch(rejectFetch(err));
      return rejectWithValue(err);
    }
  }
)

export const getCustomerOrders = createAsyncThunk(
  'customers/getCustomerOrders',
  async function({ id }, {rejectWithValue, dispatch, getState}) {
    lastCustomer = id;
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
      dispatch(rejectFetch(err));
      return rejectWithValue(err);
    }
  }
)

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
      dispatch(addTemplates({data}))
      dispatch(fulfilledFetch());
    } catch (err) {
      dispatch(rejectFetch(err));
      return rejectWithValue(err);
    }
  }
)

export const pushVoucher = createAsyncThunk(
  'customers/pushVoucher',
  async function({ email, template}, {rejectWithValue, getState, dispatch}) {
    const jwt = getState().user.userData.jwt.auth;
    dispatch(pendingFetch());
    try {
      const res = await fetch(`${baseUrl}/api/v1/order_item/${lastOrder}`, {
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
      if (!res.ok) throw new Error(`Ошибка при получении данных`);
      dispatch(fulfilledFetch());
    } catch (err) {
      return rejectWithValue(err);
      return rejectWithValue(err);
    }
  }
)

export const customersSlice = createSlice({
  name: 'customers',
  initialState: {
    customers: [],
    orders: [],
    templates: [],
  },
  reducers: {
    addCustomers(state, action) {
      state.customers = action.payload.data.results;
    },
    addOrders(state, action) {
      state.orders = action.payload.data.orders;
    },
    addTemplates(state, action) {
      state.templates = Object.entries(action.payload.data.templates).map((e) => ( { [e[0]]: e[1] } ));
    }
  }
})

export const {addCustomers, addOrders, addTemplates} = customersSlice.actions;

export default customersSlice.reducer;
