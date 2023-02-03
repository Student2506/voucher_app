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

  getCostumers() {
    return fetch(`${this._baseUrl}/api/v1/customers/`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json"
      }
    }).then(res => this._getResponseData(res));
  }

  getCustomerOrder(id) {
    return fetch(`${this._baseUrl}/api/v1/customers/${id}/`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json"
      }
    }).then(res => this._getResponseData(res));
  }
}

export default new Api({
  baseUrl: 'http://10.0.10.234'
});
