class Api {
  constructor (options) {
    this._baseUrl = options.baseUrl;
  }

  _getResponseData(res) {
    if (res.ok) {
      return res.json();
    }
    return Promise.reject(res);
  }

  getCostumers(jwt) {
    return fetch(`${this._baseUrl}/api/v1/customers/`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "Authorization": `JWT ${jwt}`,
      }
    }).then(res => this._getResponseData(res));
  }

  getCustomerOrders(id, jwt) {
    return fetch(`${this._baseUrl}/api/v1/customers/${id}/`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "Authorization": `JWT ${jwt}`,
      }
    }).then(res => this._getResponseData(res));
  }

  getOrderTemplates(id, jwt) {
    return fetch(`${this._baseUrl}/api/v1/voucher_type/${id}`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "Authorization": `JWT ${jwt}`,
      }
    }).then(res => this._getResponseData(res));
  }

  pushVouchers(id, template, email, jwt) {
    return fetch(`${this._baseUrl}/api/v1/order_item/${id}/`, {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        "Authorization": `JWT ${jwt}`,
      },
      body: JSON.stringify({
        "template": template,
        "addresses": email,
      })
    }).then(res => this._getResponseData(res))

  }
}

export default new Api({
  baseUrl: `http://${process.env.REACT_APP_MYIP}`
});
