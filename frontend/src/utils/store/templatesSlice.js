import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import {BASE_URL} from "../../constants";

export const getTemplates = createAsyncThunk(
  'templates/getTemplates',
  async function(_, {rejectWithValue, dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    try {
      const res = await fetch(`${BASE_URL}/api/v1/templates`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          "Authorization": `JWT ${jwt}`,
        }
      })
      if(!res.ok) throw new Error('Произошла ошибка')
      const data = await res.json();
      dispatch(addTemplates(data.results));
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
)

export const templatesSlice = createSlice({
  name: 'templates',
  initialState: {
    templates: [],
    status: null,
  },
  reducers: {
    addTemplates(state, action) {
      state.templates = action.payload;
    }
  },
  extraReducers: {
    [getTemplates.pending]: (state) => {
      state.status = 'loading';
    },
    [getTemplates.fulfilled]: (state) => {
      state.status = null;
    },
    [getTemplates.rejected]: (state, action) => {
      state.status = 'rejected';
    }
  }
})

export const {addTemplates} = templatesSlice.actions;

export default templatesSlice.reducer;

