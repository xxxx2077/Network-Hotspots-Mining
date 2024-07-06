import request from '@/utils/request'

// 热点榜单数据
export function getHotPointList() {
    return request({
        url: '/hotlist',
        method: 'GET'
    })
}

// 热度上升榜
export function getSpeedList() {
    return request({
        url: '/speedlist',
        method: 'GET'
    })
}

// 事件类型热度
export function getClassHotVal() {
    return request({
        url: '/classHotValue',
        method: 'GET'
    })
}

// 本周新增统计
export function getWeekAdded() {
    return request({
        url: '/weekAdded',
        method: 'GET'
    })
}