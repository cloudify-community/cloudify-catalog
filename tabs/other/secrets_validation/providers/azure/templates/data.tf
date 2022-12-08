data "azurerm_advisor_recommendations" "example" {
  filter_by_category        = ["Security", "Cost"]
}