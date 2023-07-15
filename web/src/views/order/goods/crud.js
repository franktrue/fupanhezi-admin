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
            title: '名称',
            key: 'name',
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
            title: '有效期（月）',
            key: 'month_num',
            type: 'number',
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '有效期必填' }]
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
            title: '售价',
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
          },
          {
            title: '销量',
            key: 'sale_num',
            type: "number",
            form: {
              disabled: true
            }
          },
          {
            title: '下架',
            key: 'del_flag',
            type: "radio",
            search: {
              disabled: false
            },
            dict:  {
              data: vm.dictionary('button_whether_number')
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
      ]
  };
};
