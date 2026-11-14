using Microsoft.VisualStudio.TestTools.UnitTesting;
using OrderPricing;

namespace OrderPricing.Tests;

[TestClass]
public class PriceCalculatorTests
{
    [TestMethod]
    public void RegularOrder_1000WithoutLoyalty_TotalIs1300()
    {
        decimal subtotal = 1000m;
        decimal expected = 1300m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void RegularOrder_1000WithLoyalty_TotalIs1200()
    {
        decimal subtotal = 1000m;
        decimal expected = 1200m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, true, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Discount_JustBelow5000_NoDiscount()
    {
        decimal subtotal = 4999.99m;
        decimal expected = 4999.99m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Discount_Exactly5000_DiscountIsApplied()
    {
        decimal subtotal = 5000m;
        decimal expected = 4750m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Discount_JustAbove5000_DiscountIsApplied()
    {
        decimal subtotal = 5000.01m;
        decimal expected = 4750.01m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Delivery_JustBelow4000_Costs300()
    {
        decimal subtotal = 3999.99m;
        decimal expected = 4299.99m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Delivery_Exactly4000_IsFree()
    {
        decimal subtotal = 4000m;
        decimal expected = 4000m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Delivery_Above4000_IsFree()
    {
        decimal subtotal = 4000.01m;
        decimal expected = 4000.01m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void LoyaltyAndFreeDelivery_4000_TotalIs3600()
    {
        decimal subtotal = 4000m;
        decimal expected = 3600m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, true, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void LoyaltyAndAmountDiscount_Only10PercentApplied()
    {
        decimal subtotal = 6000m;
        decimal expected = 5400m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, true, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void ExpressDelivery_1000_Costs500()
    {
        decimal subtotal = 1000m;
        decimal expected = 1500m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, false, true);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void ExpressDelivery_4500_StillCosts500()
    {
        decimal subtotal = 4500m;
        decimal expected = 5000m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, false, true);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void ZeroSubtotal_RegularDelivery_TotalIs300()
    {
        decimal subtotal = 0m;
        decimal expected = 300m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void MaximumSubtotal_100000_IsAccepted()
    {
        decimal subtotal = 100000m;
        decimal expected = 95000m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void NegativeSubtotal_ThrowsException()
    {
        Assert.ThrowsException<System.ArgumentOutOfRangeException>(() =>
            PriceCalculator.CalculateTotal(-0.01m, false, false));
    }

    [TestMethod]
    public void SubtotalAboveMaximum_ThrowsException()
    {
        Assert.ThrowsException<System.ArgumentOutOfRangeException>(() =>
            PriceCalculator.CalculateTotal(100000.01m, false, false));
    }

    [TestMethod]
    public void FractionalSubtotal_WithLoyalty_RoundsAwayFromZero()
    {
        decimal subtotal = 1000.05m;
        decimal expected = 1200.05m;

        decimal actual = PriceCalculator.CalculateTotal(
            subtotal, true, false);

        Assert.AreEqual(expected, actual);
    }
}
