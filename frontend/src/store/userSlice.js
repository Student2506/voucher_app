import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";

export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async function({login, pass}, {rejectWithValue, dispatch}) {
    try {
      const res = await fetch(`http://10.0.10.234/api/v1/auth/jwt/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          "username": login,
          "password": pass,
        })
      })

      if (!res.ok) throw new Error('Ошибка сервера!')
      const data = await res.json();
      dispatch(addUserData({jwt: data, login}))
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
)

export const updateJwt = createAsyncThunk(
  'user/updateJwt',
  async function({jwtRefresh}, {rejectWithValue, dispatch}) {
    try {
      const res = await fetch(`http://10.0.10.234/api/v1/auth/jwt/refresh/`, {
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
      dispatch(refreshJwt(data))
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
    addUserData(state, action) {
      state.userData = {
        login: action.payload.login,
        jwt: {
          auth: action.payload.jwt.access,
          refr: action.payload.jwt.refresh,
        }
      };
    },
    refreshJwt(state, action) {
      state.userData.jwt.auth = action.payload.access;
    }
  },
  extraReducers: {
    [fetchUser.pending]: (state, action) => {
      state.status = 'Loading';
      state.error = null;
      state.loggedIn = false;
    },
    [fetchUser.fulfilled]: (state, action) => {
      state.status = 'resolved';
      state.loggedIn = true;
    },
    [fetchUser.rejected]: (state, action) => {
      state.status = 'rejected';
      state.error = action.payload;
    },
  }
})

const {addUserData, refreshJwt} = userSlice.actions;

export default userSlice.reducer;
