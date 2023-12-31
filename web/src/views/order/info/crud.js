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
          },
          custom: [
            {
              thin: true,
              text: '子订单',
              size: 'small',
              type: 'success',
              icon: 'el-icon-bangzhu',
              show () {
                return vm.hasPermissions('item')
              },
              emit: 'orderItem'
            },
          ]
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
            fixed: 'left',
            title: "订单号",
            key: "order_no",
            type: "input",
            search: true,
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '订单号必填' }]
            }
          },
          {
            title: '用户ID',
            key: 'user_id',
            type: "number",
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '用户ID必填' }]
            }
          },
          {
            title: '支付方式',
            key: 'payment_way',
            type: 'radio',
            search: {
              disabled: false
            },
            dict:  {
              data: vm.dictionary('order_payment_way')
            },
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '支付方式必填' }]
            }
          },
          {
            title: '是否支付',
            key: 'is_pay',
            type: 'radio',
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
              rules: [{ required: true, message: '是否支付必填' }]
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
          },
          {
            title: '支付时间',
            key: 'payment_time',
            type: 'datetime',
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '创建时间',
            key: 'create_datetime',
            type: 'datetime',
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          }
      ]
  };
};
