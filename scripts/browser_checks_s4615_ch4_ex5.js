(() => {
  "use strict";

  const BASE = "/sap/opu/odata/sap";
  const checks = [
    { name: "COMPANY_CODE", value: "1010", service: "API_COMPANYCODE_SRV", entitySet: "A_CompanyCode", filters: { CompanyCode: "1010" }, select: ["CompanyCode"] },
    { name: "SALES_ORGANIZATION", value: "1010", service: "API_SALESORGANIZATION_SRV", entitySet: "A_SalesOrganization", filters: { SalesOrganization: "1010" }, select: ["SalesOrganization"] },
    { name: "DISTRIBUTION_CHANNEL", value: "10", service: "API_DISTRIBUTIONCHANNEL_SRV", entitySet: "A_DistributionChannel", filters: { DistributionChannel: "10" }, select: ["DistributionChannel"] },
    { name: "ORGANIZATION_DIVISION", value: "00", service: "API_DIVISION_SRV", entitySet: "A_Division", filters: { Division: "00" }, select: ["Division"] },
    { name: "CUSTOMER_TEMPLATE_A00_BP", value: "C615-A00", service: "API_BUSINESS_PARTNER", entitySet: "A_BusinessPartner", filters: { BusinessPartner: "C615-A00" }, select: ["BusinessPartner"], evidenceFields: ["BusinessPartnerGrouping", "OrganizationBPName1"] },
    { name: "CUSTOMER_TEMPLATE_A00_COMPANY", value: "C615-A00|1010", service: "API_BUSINESS_PARTNER", entitySet: "A_CustomerCompany", filters: { Customer: "C615-A00", CompanyCode: "1010" }, select: ["Customer", "CompanyCode"], evidenceFields: ["ReconciliationAccount", "PaymentTerms"] },
    { name: "CUSTOMER_TEMPLATE_A00_SALES_AREA", value: "C615-A00|1010/10/00", service: "API_BUSINESS_PARTNER", entitySet: "A_CustomerSalesArea", filters: { Customer: "C615-A00", SalesOrganization: "1010", DistributionChannel: "10", Division: "00" }, select: ["Customer", "SalesOrganization", "DistributionChannel", "Division"], evidenceFields: ["Currency", "ShippingCondition", "SupplyingPlant", "IncotermsClassification", "IncotermsLocation1", "CustomerAccountAssignmentGroup", "CustomerPricingProcedure"] },
    { name: "CUSTOMER_TEMPLATE_B00_BP", value: "C615-B00", service: "API_BUSINESS_PARTNER", entitySet: "A_BusinessPartner", filters: { BusinessPartner: "C615-B00" }, select: ["BusinessPartner"], evidenceFields: ["BusinessPartnerGrouping", "OrganizationBPName1"] },
    { name: "CUSTOMER_TEMPLATE_B00_COMPANY", value: "C615-B00|1010", service: "API_BUSINESS_PARTNER", entitySet: "A_CustomerCompany", filters: { Customer: "C615-B00", CompanyCode: "1010" }, select: ["Customer", "CompanyCode"], evidenceFields: ["ReconciliationAccount", "PaymentTerms"] },
    { name: "CUSTOMER_TEMPLATE_B00_SALES_AREA", value: "C615-B00|1010/10/00", service: "API_BUSINESS_PARTNER", entitySet: "A_CustomerSalesArea", filters: { Customer: "C615-B00", SalesOrganization: "1010", DistributionChannel: "10", Division: "00" }, select: ["Customer", "SalesOrganization", "DistributionChannel", "Division"], evidenceFields: ["Currency", "ShippingCondition", "SupplyingPlant", "IncotermsClassification", "IncotermsLocation1", "CustomerAccountAssignmentGroup", "CustomerPricingProcedure"] },
    { name: "CUSTOMER_BP_ROOT", value: "C615-D00", service: "API_BUSINESS_PARTNER", entitySet: "A_BusinessPartner", filters: { BusinessPartner: "C615-D00" }, select: ["BusinessPartner"] },
    { name: "CUSTOMER_ROLE", value: "C615-D00", service: "API_BUSINESS_PARTNER", entitySet: "A_Customer", filters: { Customer: "C615-D00" }, select: ["Customer"] },
    { name: "CUSTOMER_SALES_AREA", value: "C615-D00|1010/10/00", service: "API_BUSINESS_PARTNER", entitySet: "A_CustomerSalesArea", filters: { Customer: "C615-D00", SalesOrganization: "1010", DistributionChannel: "10", Division: "00" }, select: ["Customer", "SalesOrganization", "DistributionChannel", "Division"] },
    { name: "PRODUCT_ROOT", value: "P615-400", service: "API_PRODUCT_SRV", entitySet: "A_Product", filters: { Product: "P615-400" }, select: ["Product"] },
    { name: "PRODUCT_UOM", value: "P615-400|PC", service: "API_PRODUCT_SRV", entitySet: "A_ProductUnitsOfMeasure", filters: { Product: "P615-400", AlternativeUnit: "PC" }, select: ["Product", "AlternativeUnit"] },
    { name: "PRODUCT_TEMPLATE_100", value: "P615-100", service: "API_PRODUCT_SRV", entitySet: "A_Product", filters: { Product: "P615-100" }, select: ["Product"], evidenceFields: ["ProductType", "IndustrySector", "BaseUnit"] },
    { name: "PRODUCT_TEMPLATE_100_PLANT", value: "P615-100", service: "API_PRODUCT_SRV", entitySet: "A_ProductPlant", filters: { Product: "P615-100" }, select: ["Product", "Plant"], evidenceFields: ["AvailabilityCheckType"] },
    { name: "PRODUCT_TEMPLATE_100_SALES", value: "P615-100|1010/10", service: "API_PRODUCT_SRV", entitySet: "A_ProductSalesDelivery", filters: { Product: "P615-100", ProductSalesOrg: "1010", ProductDistributionChnl: "10" }, select: ["Product", "ProductSalesOrg", "ProductDistributionChnl"], evidenceFields: ["SupplyingPlant", "ItemCategoryGroup", "AccountDetnProductGroup"] },
    { name: "PRODUCT_TEMPLATE_100_UOM", value: "P615-100|PC", service: "API_PRODUCT_SRV", entitySet: "A_ProductUnitsOfMeasure", filters: { Product: "P615-100", AlternativeUnit: "PC" }, select: ["Product", "AlternativeUnit"], evidenceFields: ["QuantityNumerator", "QuantityDenominator"] },
    { name: "PRODUCT_TEMPLATE_200", value: "P615-200", service: "API_PRODUCT_SRV", entitySet: "A_Product", filters: { Product: "P615-200" }, select: ["Product"], evidenceFields: ["ProductType", "IndustrySector", "BaseUnit"] },
    { name: "PRODUCT_TEMPLATE_200_PLANT", value: "P615-200", service: "API_PRODUCT_SRV", entitySet: "A_ProductPlant", filters: { Product: "P615-200" }, select: ["Product", "Plant"], evidenceFields: ["AvailabilityCheckType"] },
    { name: "PRODUCT_TEMPLATE_200_SALES", value: "P615-200|1010/10", service: "API_PRODUCT_SRV", entitySet: "A_ProductSalesDelivery", filters: { Product: "P615-200", ProductSalesOrg: "1010", ProductDistributionChnl: "10" }, select: ["Product", "ProductSalesOrg", "ProductDistributionChnl"], evidenceFields: ["SupplyingPlant", "ItemCategoryGroup", "AccountDetnProductGroup"] },
    { name: "PRODUCT_TEMPLATE_200_UOM", value: "P615-200|PC", service: "API_PRODUCT_SRV", entitySet: "A_ProductUnitsOfMeasure", filters: { Product: "P615-200", AlternativeUnit: "PC" }, select: ["Product", "AlternativeUnit"], evidenceFields: ["QuantityNumerator", "QuantityDenominator"] },
    { name: "DUPLICATE_CASH_SALE", value: "BV|1010/10/00|C615-D00|00S4615-BV", service: "API_SALES_ORDER_SRV", entitySet: "A_SalesOrder", filters: { SalesOrderType: "BV", SalesOrganization: "1010", DistributionChannel: "10", OrganizationDivision: "00", SoldToParty: "C615-D00", PurchaseOrderByCustomer: "00S4615-BV" }, select: ["SalesOrder", "SalesOrderType", "SalesOrganization", "DistributionChannel", "OrganizationDivision", "SoldToParty", "PurchaseOrderByCustomer"], invert: true }
  ];

  const escapeLiteral = value => String(value).replace(/'/g, "''");
  const results = [];
  const metadataCache = new Map();

  async function read(url, accept) {
    const response = await fetch(url, {
      method: "GET",
      credentials: "include",
      headers: { Accept: accept }
    });
    if (response.status === 401 || response.status === 403) {
      throw new Error(`Authentication stopped validation (${response.status})`);
    }
    return response;
  }

  async function metadata(service) {
    if (!metadataCache.has(service)) {
      const response = await read(`${BASE}/${service}/$metadata`, "application/xml");
      if (!response.ok) throw new Error(`${service} metadata HTTP ${response.status}`);
      metadataCache.set(service, new DOMParser().parseFromString(await response.text(), "application/xml"));
    }
    return metadataCache.get(service);
  }

  function entityProperties(doc, entitySetName) {
    const sets = [...doc.getElementsByTagNameNS("*", "EntitySet")];
    const set = sets.find(node => node.getAttribute("Name") === entitySetName);
    if (!set) return null;
    const qualifiedType = set.getAttribute("EntityType") || "";
    const typeName = qualifiedType.split(".").pop();
    const types = [...doc.getElementsByTagNameNS("*", "EntityType")];
    const type = types.find(node => node.getAttribute("Name") === typeName);
    if (!type) return null;
    return new Set([...type.getElementsByTagNameNS("*", "Property")].map(node => node.getAttribute("Name")));
  }

  async function runCheck(check) {
    const doc = await metadata(check.service);
    const available = entityProperties(doc, check.entitySet);
    const required = [...Object.keys(check.filters), ...check.select];
    if (!available || !required.every(name => available.has(name))) {
      return { PRECHECK: check.name, VALUE: check.value, SERVICE: check.service, ENTITYSET: check.entitySet, HTTP: "METADATA_ONLY", RESULT: "NEEDS_LIVE_VALIDATION" };
    }
    const evidenceFields = (check.evidenceFields || []).filter(name => available.has(name));
    const selectedFields = [...new Set([...check.select, ...evidenceFields])];
    const filter = Object.entries(check.filters).map(([key, value]) => `${key} eq '${escapeLiteral(value)}'`).join(" and ");
    const query = new URLSearchParams({ "$filter": filter, "$select": selectedFields.join(","), "$top": "1", "$format": "json" });
    const response = await read(`${BASE}/${check.service}/${check.entitySet}?${query.toString()}`, "application/json");
    if (!response.ok) return { PRECHECK: check.name, VALUE: check.value, SERVICE: check.service, ENTITYSET: check.entitySet, HTTP: response.status, RESULT: "NEEDS_LIVE_VALIDATION" };
    const body = await response.json();
    const rows = body && body.d ? (Array.isArray(body.d.results) ? body.d.results : [body.d]) : [];
    const found = rows.length > 0;
    const result = check.invert ? (found ? "DUPLICATE_FOUND_BLOCKED" : "CONFIRMED_CLEAR") : (found ? "CONFIRMED_FOUND" : "CONFIRMED_NOT_FOUND");
    const evidence = found ? Object.fromEntries(evidenceFields.map(name => [name, rows[0][name] ?? null])) : {};
    return { PRECHECK: check.name, VALUE: check.value, SERVICE: check.service, ENTITYSET: check.entitySet, HTTP: response.status, RESULT: result, EVIDENCE: evidence };
  }

  (async () => {
    results.push({ PRECHECK: "SALES_AREA", VALUE: "1010/10/00", SERVICE: "BAPI_SALES_AREAS_GET", ENTITYSET: "N/A", HTTP: "NOT_RUN", RESULT: "NEEDS_LIVE_VALIDATION" });
    results.push({ PRECHECK: "PRODUCT_SALES_VIEW", VALUE: "P615-400|1010/10", SERVICE: "API_PRODUCT_SRV", ENTITYSET: "NOT_CONFIRMED", HTTP: "METADATA_ONLY", RESULT: "NEEDS_LIVE_VALIDATION" });
    for (const check of checks) results.push(await runCheck(check));
    console.table(results);
    console.log(
      results
        .map(r => `${r.PRECHECK} | ${r.VALUE} | ${r.HTTP} | ${r.RESULT}`)
        .join("\n")
    );
    return results;
  })().catch(error => {
    console.table(results);
    console.error(String(error.message || error));
  });
})();
