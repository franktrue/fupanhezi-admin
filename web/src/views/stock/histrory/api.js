import { request } from '@/api/service'
export const urlPrefix = '/api/stock/history/'

export function GetList(query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}

export function AddObj(obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}

export function UpdateObj(obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}

export function DelObj(id) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete',
    data: { id }
  })
}

// 抓取指定股票行情
export function FetchData(obj) {
  return request({
    url: urlPrefix + "fetch/",
    method: 'post',
    data: obj
  })
}

export function UpdateLatest() {
  return request({
    url: urlPrefix + 'latest/',
    method: 'post'
  })
}

export function UpdateAuction(obj) {
  return request({
    url: urlPrefix + 'update_auction/',
    method: 'post',
    data: obj
  })
}

export function SearchStocks(query) {
  return request({
    url: urlPrefix+'search_stocks/',
    method: 'get',
    params: query
  })
}
