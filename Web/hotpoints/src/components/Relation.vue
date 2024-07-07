<template>
    <div style="width: 100%; height: 100%;">
        <RelationGraph ref="graphRef" :options="graphOption"></RelationGraph>
    </div>
</template>

<script>
import RelationGraph from 'relation-graph'
export default {
    name: 'Relation',
    components: {
        RelationGraph,
    },
    props: {
        nodeData: { type: Array, required: true },
        lineData: { type: Array, required: true }
    },
    data() {
        return {
            graphOption: {
                debug: false,
                defaultNodeBorderWidth: 0,
                allowSwitchLineShape: true,
                allowSwitchJunctionPoint: true,
                defaultLineShape: 1,
                'layouts': [
                    {
                        'label': '自动布局',
                        'layoutName': 'force',
                        'layoutClassName': 'seeks-layout-force'
                    }
                ],
                defaultJunctionPoint: 'border'
            }
        }
    },
    mounted() {
        this.showGraph(this.$props.nodeData, this.$props.lineData);
    },
    beforeDestroy() {
        this.$refs.graphRef.getInstance().stopAutoLayout();
    },
    methods: {
        showGraph(node, line) {
            if (node.length === 0) {
                node.push({ id: '1', text: '话题内帖子没有强相关关系' });
            }
            const jsonData = {
                rootId: 'a',
                nodes: node,
                lines: line,
            }

            this.$refs.graphRef.setJsonData(jsonData, (graphInstance) => {
                graphInstance.setZoom(100);
            });
        },
    },
    watch: {
        nodeData(newVal) {
            this.showGraph(newVal, this.$props.lineData);
        }
    }
}
</script>