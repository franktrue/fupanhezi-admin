export const crudOptions = vm => {
  return {
      pageOptions: {
          compact: true
      },
      options: {
          tableType: "vxe-table",
          rowKey: true, // 必须设置，true or false
          rowId: "id",
          height: "100%", // 表格高度100%, 使用toolbar必须设置
          highlightCurrentRow: false
      },
      rowHandle: {
          width: 140,
          view: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Retrieve");
              }
          },
          edit: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Update");
              }
          },
          remove: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Delete");
              }
          }
      },
      indexRow: false,
      viewOptions: {
          componentType: "form"
      },
      formOptions: {
          defaultSpan: 24, // 默认的表单 span
          width: "35%"
      },
      columns: [
          {
            title: 'SPU名称',
            key: 'spu_name',
            type: "input",
            search: true,
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: 'spu_name必填' }]
            }
          },
          {
            title: '数量',
            key: 'num',
            type: 'number',
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '数量必填' }]
            }
          },
          {
            title: '状态',
            key: 'status',
            type: "select",
            search: {
              disabled: false
            },
            dict:  {
              data: vm.dictionary('order_status')
            },
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '状态必填' }]
            }
          },
          {
            title: '市场价',
            key: 'sales_price',
            type: "number",
            form: {
              component: {
                name: 'el-input-number',
                props: {
                  precision: 2
                }
              },
              scopedSlots: {
                prefix: () => '￥'
              },
              rules: [{ required: true, message: '市场价必填' }]
            }
          },
          {
            title: '支付价',
            key: 'payment_price',
            type: "number",
            form: {
              component: {
                name: 'el-input-number',
                props: {
                  precision: 2
                }
              },
              scopedSlots: {
                prefix: () => '￥'
              },
              rules: [{ required: true, message: '支付价' }]
            }
          }
      ]
  };
};
