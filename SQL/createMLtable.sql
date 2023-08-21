CREATE TABLE shipmentsml AS
SELECT 
    `Category Id`,
    `Customer City`,
    `Customer Country`,
    `Order City`,
    `Order Country`,
    `Shipping Mode`,
    `Shipping Cost`,
    Distance
FROM augmentedshipments;
