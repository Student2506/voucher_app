import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import {BASE_URL} from "../../constants";
import jwt_decode from "jwt-decode";

const decodeJwt = (token) => jwt_decode(token);

export const updateJwt = createAsyncThunk(
  'user/updateJwt',
  async function({jwtRefresh}, {rejectWithValue, dispatch}) {
    try {
      const res = await fetch(`${BASE_URL}/api/v1/auth/jwt/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          refresh: jwtRefresh,
        })
      })
      if(!res.ok) throw new Error('Ошибка(((')
      const data = await res.json();
      dispatch(refreshJwt({data, jwtRefresh}))
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
)

export const userSlice = createSlice({
  name: 'user',
  initialState: {
    userData: {},
    status: null,
    loggedIn: false,
    error: null,
  },
  reducers: {
    refreshJwt(state, action) {
      const { user_id } = decodeJwt(action.payload.data.access);
      state.userData = {
        login: user_id,
        jwt: {
          auth: action.payload.data.access,
          refr: action.payload.jwtRefresh,
        }
      }
    },
  },
  extraReducers: {
    [updateJwt.pending]: (state) => {
      state.status = 'Loading';
      state.error = null;
    },
    [updateJwt.fulfilled]: (state) => {
      state.status = 'resolved';
      if (!state.loggedIn) {
        state.loggedIn = true;
      }
    },
    [updateJwt.rejected]: (state, action) => {
      state.status = 'rejected';
      state.error = action.payload;
    }
  }
})

export const {refreshJwt} = userSlice.actions;

export default userSlice.reducer;

