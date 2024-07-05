import request from '@/utils/request'

// 获取话题详情
export function getTopicDetail(id) {
    return request({
        url: '/topic/details',
        method: 'GET',
        params: {
            topicId: id
        }
    })
}