from cocotb.triggers import Timer


async def reset_dut(dut, t_up=1750, t_low=250):
    # reset cpu
    dut.reset.value = 1
    await Timer(t_up, units="ps")
    dut.reset.value = 0
    await Timer(t_low, units="ps")
