import { useEffect } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { serializeDateTime, deserializeDateTime } from "@web/core/l10n/dates";

import { SaleOrderLineProductField } from "@sale/js/sale_product_field";
import {ApiProductConfiguratorDialog} from "./api_product_configurator_dialog";


patch(SaleOrderLineProductField.prototype, {

    /** override **/
    onEditConfiguration() {
        if (this.isApiConfigurtion) {
            this._openApiProductConfigurator(true);
        } else if (this.isCombo) {
            this._openComboConfigurator(true);
        } else if (this.isConfigurableTemplate) {
            this._openProductConfigurator(true);
        } 
    },
    /**
     * standard implementation
     * 
     */
    get isApiConfigurtion() {
        return this.props.record.data.is_api_configurator;
    },
    get api_configurator_value() {
        if(this.props.record.data.api_configurator_value){
            return JSON.parse(this.props.record.data.api_configurator_value);
        }
        return {};
    },
    get api_node_engine_name(){
        return this.props.record.data.api_node_engine_name;
    },
    get product_id(){
        return this.props.record.data.product_id.id;
    },


    async _openApiProductConfigurator(edit = false, selectedComboItems = []) {
        const saleOrderRecord = this.props.record.model.root;
        const saleOrderLine = this.props.record.data;
        this.dialog.add(ApiProductConfiguratorDialog, {
            api_configurator_value: this.api_configurator_value,
            api_node_engine_name:this.api_node_engine_name,
            product_id: this.product_id,
            //
            save : async (api_configurator_value) => {
                  var attr_name = ''
                  for (var key in api_configurator_value) {
                        attr_name = attr_name + "\n" + key + ":" + api_configurator_value[key];
                    }
                  
                   this.props.record.update({
                       name :attr_name,
                       api_configurator_value:JSON.stringify(api_configurator_value)
                   });
            },
        });

    }
});

